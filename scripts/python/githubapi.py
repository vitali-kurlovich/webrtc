import logging
import os
from datetime import datetime

import requests
from exceptions import RequestException


class PullRequestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.message} status code: {self.status_code}"


class UploadRequestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.message} status code: {self.status_code}"


class GitHubApiRepository:
    def __init__(self, repo, token):
        super().__init__()
        self.baseUrl = "https://api.github.com"
        self.repo = repo
        self.token = token

        self.logger = logging.getLogger(__name__)

    def releasesURL(self):
        return f"{self.baseUrl}/repos/{self.repo}/releases"

    def pullURL(self):
        return f"{self.baseUrl}/repos/{self.repo}/pulls"

    def requestHeader(self):
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }

    def fetchReleases(self):
        self.logger.debug(f"Fetch repo ({self.repo}) releases.")
        try:
            response = requests.get(
                self.releasesURL(),
                headers=self.requestHeader(),
            )
            response.raise_for_status()
            releases = response.json()
            self.logger.debug(f"Releases: {releases}")
            return releases
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed to fetch releases: {error}")
            raise RequestException("Failed to fetch releases", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)

    def fetchLastRelease(self):
        self.logger.info("Fetch last release.")
        releases = self.fetchReleases()

        if len(releases) == 0:
            return (-1, None)

        if releases[0]["published_at"] is None:
            return (-1, None)

        version = int(releases[0]["tag_name"].split(".")[1])
        date = datetime.fromisoformat(releases[0]["published_at"].replace("Z", ""))

        self.logger.info(f"Latest release: version {version}, date: {date}")

        return (version, date)

    def postReleaseDraft(self, fields):
        self.logger.debug(f"Post release with fields: {fields}")
        try:
            response = requests.post(
                self.releasesURL(), json=fields, headers=self.requestHeader()
            )
            response.raise_for_status()
            body = response.json()
            self.logger.debug(f"Post release body: {body}")
            return body
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed post release draft: {error}")
            raise RequestException("Failed post release draft", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)

    def createPullRequest(self, body):
        self.logger.debug(f"Create pull request with: {body}")
        try:
            response = requests.post(
                self.pullURL(), json=body, headers=self.requestHeader()
            )
            response.raise_for_status()

            success = response.status_code == requests.codes.created
            if not success:
                self.logger.error(
                    f"Pull request failed with status code: {response.status_code}"
                )
                raise PullRequestError("Pull request failed", response.status_code)

        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed post release draft: {error}")
            raise RequestException("Failed post release draft", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)

    def uploadReleaseAsset(self, url, assetLocalPath, assetName):
        self.logger.debug(
            f"Upload asset with name: {assetName}, url: {url}, asset path: {assetLocalPath} "
        )
        try:
            url = url.replace("{?name,label}", "")
            fileToUpload = open(assetLocalPath, "rb")
            size = os.stat(assetLocalPath).st_size
            params = {"name": assetName}

            headers = self.requestHeader()
            headers["Content-Length"] = str(size)
            headers["Content-Type"] = "application/zip"

            response = requests.post(
                url, params=params, data=fileToUpload, headers=headers
            )
            response.raise_for_status()

            body = response.json()

            self.logger.debug(f"uploadReleaseAsset body: {body}")

            for key, value in body.items():
                self.logger.debug(f"{key}= {value}")

            success = response.status_code == requests.codes.created

            if not success:
                self.logger.error(
                    f"Upload request failed with status code: {response.status_code}"
                )
                raise UploadRequestError("Upload request failed", response.status_code)

            return body

        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Upload release assert: {error}")
            raise RequestException("Failed upload assert", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)
