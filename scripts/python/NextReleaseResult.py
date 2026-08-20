from dataclasses import dataclass
from datetime import datetime

@dataclass
class NextReleaseResult:
    version: int
    releaseDate: datetime
    branch: str
