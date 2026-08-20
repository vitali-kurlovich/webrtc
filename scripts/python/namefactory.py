from typing_extensions import final

from . import NextReleaseResult

@final
class NameFactory:
    def __init__(self, major: str, patch: str):
        super().__init__()

        self.major = major
        self.patch = patch

    def tagRelease(self, release: NextReleaseResult):
        return f"{self.major}.{release.version}.{self.patch}"

    def releaseBranchName(self, release: NextReleaseResult):
         return f"release-v{nextRelease.version}"
