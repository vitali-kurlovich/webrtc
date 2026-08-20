import logging
import os
import sys

from ReleaseManager import ReleaseManager


def main():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True

    logger = logging.getLogger(__name__)

    manager = ReleaseManager(major="0", patch="0")
    try:
        manager.run()
    except Exception as error:
        logger.error(f"Error {error}")
        os._exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
