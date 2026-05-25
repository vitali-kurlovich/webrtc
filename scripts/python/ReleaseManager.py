import json
import logging
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta

import git
import requests
from chromiumdash import ChromiumdashRepository
from githubapi import GitHubApiRepository
from Metadata import Metadata
from template import TemplateBuilder


@dataclass
class NextReleaseResult:
    version: int
    releaseDate: datetime
    branch: str


class ReleaseManagerException(Exception):
    pass


class ShellException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.message} return: ({self.code})"


class ReleaseManager:
    def __init__(self, major: str, patch: str):
        super().__init__()

        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        if GITHUB_TOKEN is None:
            raise ReleaseManagerException("GITHUB_TOKEN is not set")

        GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY")
        if GITHUB_REPO is None:
            raise ReleaseManagerException("GITHUB_REPOSITORY is not set")

        self.repo = GITHUB_REPO
        self.major = major
        self.patch = patch
        self.gitHubApi = GitHubApiRepository(repo=GITHUB_REPO, token=GITHUB_TOKEN)
        self.chromiumDashApi = ChromiumdashRepository()

        self.isDebug = os.environ.get("BUILD_DEBUG") == "1"

        self.logger = logging.getLogger(__name__)

        rootDir = os.environ.get("ROOT_DIR")
        if rootDir is None:
            raise ReleaseManagerException("ROOT_DIR is not set")

        self.rootDir = rootDir

        artifactDir = os.environ.get("OUTPUT_ARTIFACTS_DIR")
        if artifactDir is None:
            raise ReleaseManagerException("OUTPUT_ARTIFACTS_DIR is not set")

        self.artifactDir = artifactDir

    def run(self):

        self.logger.info("Fetch next version...")
        nextRelease = self._getNextRelease()

        if not self._isReleaseAvailable(nextRelease):
            self.logger.info("Next version is not out yet. Skipping build")
            os._exit(os.EX_OK)

        self.logger.info(f"New version ({nextRelease.version}) is available to build")
        self._build(nextRelease.branch)
        self.logger.info("WebRTC build successful")

        metadata = self._buildMetadata(self.artifactDir)

        self.logger.info("Creating new release draft...")
        draft = self._createReleaseDraft(nextRelease, metadata)

        self.logger.info("Upload asset to github...")

        assetName = f"WebRTC-v{nextRelease.version}.xcframework.zip"

        if self.isDebug:
            assetName = f"WebRTC-v{nextRelease.version}-debug.xcframework.zip"

        self._uploadReleaseAsset(self.artifactDir, draft, metadata, assetName)

        releaseBranch = self._createLocalBranch(nextRelease)

        self._generatePackage(nextRelease, metadata, assetName)
        self._generateReadme(nextRelease)

        self._commitChanges(releaseBranch, nextRelease)

        self._pullRequest(nextRelease, releaseBranch)

        self.logger.info("Done.")

    def _build(self, branch: str):
        os.environ["BRANCH"] = branch
        process = subprocess.run(["sh", "scripts/build.sh"])
        result = process.returncode
        if result != 0:
            raise ShellException(
                f"Build script return non-zero exit code: {result}", result
            )

    def _tagRelease(self, release: NextReleaseResult):
        return f"{self.major}.{release.version}.{self.patch}"

    def _createReleaseDraft(self, release: NextReleaseResult, metadata: Metadata):
        body = f"Release notes: https://webrtc.googlesource.com/src.git/+log/refs/{metadata.branch}/\n"
        body += f"WebRTC Branch: [{metadata.branch}](https://chromium.googlesource.com/external/webrtc/+log/{metadata.branch})\n"
        body += f"WebRTC Commit: `{metadata.commit}`\n\n"
        body += f"SHA 256 checksum: `{metadata.checksum}`\n"

        tag = self._tagRelease(release)

        fields = {
            "name": f"v{release.version}",
            "tag_name": tag,
            "draft": True,
            "body": body,
        }

        return self.gitHubApi.postReleaseDraft(fields)

    def _uploadReleaseAsset(
        self, releaseDir: str, releaseDraft, metadata: Metadata, assetName: str
    ):
        assetPath = os.path.join(releaseDir, metadata.filename)
        uploadURL = releaseDraft["upload_url"]
        self.gitHubApi.uploadReleaseAsset(uploadURL, assetPath, assetName)
        self.logger.info(
            f"Successfully created new draft release in github: {releaseDraft['url']}"
        )

    def _createLocalBranch(self, nextRelease: NextReleaseResult):
        releaseBranch = f"release-v{nextRelease.version}"
        self.logger.info(f"Creating local branch: {releaseBranch}")
        git.checkout(releaseBranch)
        return releaseBranch

    def _generatePackage(
        self,
        release: NextReleaseResult,
        metadata: Metadata,
        assetName: str,
    ):
        self.logger.info("Update Package.swift")

        packageName = self.repo.split("/")[1]

        baseUrl = f"https://github.com/{self.repo}"

        tag = self._tagRelease(release)

        url = f"{baseUrl}/releases/download/{tag}/{assetName}"

        template_path = f"{self.rootDir}/templates/Package.swift"

        builder = TemplateBuilder(template_path)

        builder.append("name", packageName)
        builder.append("url", url)
        builder.append("checksum", metadata.checksum)

        outputPath = f"{self.rootDir}/Package.swift"

        builder.write(outputPath)
        return outputPath

    def _generateReadme(
        self,
        release: NextReleaseResult,
    ):
        template_path = f"{self.rootDir}/templates/README.md"
        tag = self._tagRelease(release)

        builder = TemplateBuilder(template_path)

        builder.append("repo", self.repo)
        builder.append("tag", tag)

        if self.isDebug:
            builder.append("build_flag", "✅")
        else:
            builder.append("build_flag", "⛔️")

        outputPath = f"{self.rootDir}/README.md"
        builder.write(outputPath)
        return outputPath

    def _commitChanges(self, releaseBranch: str, nextRelease: NextReleaseResult):
        self.logger.info("Commiting and pushing code to remote")
        git.add("Package.swift")
        git.add("README.md")
        git.commit(f'"Updated files for release v{nextRelease.version}"')
        git.push(releaseBranch)

    def _pullRequest(self, release, head):
        self.logger.info("Create Pull Request")

        body = {
            "title": f"Release v{release.version}",
            "head": head,
            "base": "main",
            "body": f"Updated files for release v{release.version}.",
        }

        self.gitHubApi.createPullRequest(body)

    def _getNextRelease(self):
        (latestReleaseVersion, latestReleaseDate) = self.gitHubApi.fetchLastRelease()
        stableMilestone = self.chromiumDashApi.fetchStableMilestone()

        # Get the current stable milestone
        nextReleaseVersion = max(latestReleaseVersion + 1, stableMilestone)
        if nextReleaseVersion > latestReleaseVersion + 1:
            self.logger.info(
                f"Current stable milestone is {stableMilestone}, skipping ahead from {latestReleaseVersion + 1}"
            )

        milestones = self.chromiumDashApi.fetchMilestoneSchedule(nextReleaseVersion)
        releases = self.chromiumDashApi.fetchMilestoneReleases(nextReleaseVersion)

        nextReleaseDate = datetime.fromisoformat(
            milestones["mstones"][0]["stable_date"]
        )
        nextReleaseBranch = "branch-heads/" + releases[0]["webrtc_branch"]

        self.logger.info(
            f"Next release: version {nextReleaseVersion}, date: {nextReleaseDate}, branch: {nextReleaseBranch}"
        )

        return NextReleaseResult(
            version=nextReleaseVersion,
            releaseDate=nextReleaseDate,
            branch=nextReleaseBranch,
        )

    def _isReleaseAvailable(self, release):
        return datetime.today() >= (release.releaseDate + timedelta(days=1))

    def _buildMetadata(self, outputDir: str):
        with open(f"{outputDir}/metadata.json", "r") as f:
            jsonData = json.loads(f.read())
            return Metadata(
                filename=jsonData["file"],
                checksum=jsonData["checksum"],
                commit=jsonData["commit"],
                branch=jsonData["branch"],
            )
