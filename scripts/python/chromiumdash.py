import logging

import requests
from exceptions import RequestException


class NoStableMilestone(Exception):
    pass


class ChromiumdashRepository:
    def __init__(self):
        super().__init__()
        self.baseUrl = "https://chromiumdash.appspot.com/"
        self.logger = logging.getLogger(__name__)

    def fetchStableMilestone(self):
        try:
            self.logger.info("Fetch milestones.")
            response = requests.get(f"{self.baseUrl}/fetch_milestones")

            response.raise_for_status()

            milestones = response.json()
            self.logger.debug(f"Milestones. {milestones}")

            stable = [m for m in milestones if m.get("schedule_phase") == "stable"]
            if stable:
                return int(max(stable, key=lambda m: m["milestone"])["milestone"])
            else:
                self.logger.error("No milestone with schedule_phase 'stable' found")
                raise NoStableMilestone(
                    "No milestone with schedule_phase 'stable' found"
                )

        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed to fetch stable milestone: {error}")
            raise RequestException("Failed to fetch stable milestone", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)

    def fetchMilestoneSchedule(self, nextReleaseVersion):
        try:
            self.logger.info(
                f"Fetch milestone schedule where mstone={nextReleaseVersion}"
            )
            respond = requests.get(
                f"{self.baseUrl}/fetch_milestone_schedule?mstone={nextReleaseVersion}"
            )
            respond.raise_for_status()
            schedule = respond.json()
            self.logger.debug(f"Milestone schedule: {schedule}")
            return schedule
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed to fetch milestone schedule: {error}")
            raise RequestException("Failed to fetch milestone schedule", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)

    def fetchMilestoneReleases(self, nextReleaseVersion):
        try:
            self.logger.info(
                f"Fetch milestone releases where mstone={nextReleaseVersion}"
            )
            respond = requests.get(
                f"{self.baseUrl}/fetch_milestones?mstone={nextReleaseVersion}"
            )
            respond.raise_for_status()
            releases = respond.json()
            self.logger.debug(f"Milestone releases: {releases}")
            return releases
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            self.logger.error(f"Failed to fetch milestone releases: {error}")
            raise RequestException("Failed to fetch milestone releases", error)
        except Exception as error:
            self.logger.error(f"Error {error}")
            raise RequestException("Error", error)
