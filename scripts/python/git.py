import logging
import subprocess

_logger = logging.getLogger(__name__)


def checkout(branch: str):
    if len(branch) == 0:
        _logger.error("Branch name cannot be empty.")
        raise Exception("Branch name cannot be empty.")

    _run(["checkout", "-b", branch])


def add(files):
    if len(files) == 0:
        _logger.error("Files cannot be empty.")
        raise Exception("Files cannot be empty.")

    args = ["add"]

    if isinstance(files, str):
        args.append(files)
    elif isinstance(files, (tuple, list)):
        args.extend(files)
    else:
        _logger.error("Argument files must be str, list or tuple")
        raise Exception("Argument files must be str, list or tuple")

    _run(args)


def commit(message: str):
    if len(message) == 0:
        _logger.error("Message cannot be empty.")
        raise Exception("Message cannot be empty.")
    _run(["commit", "-m", message])


def push(branch: str):
    if len(branch) == 0:
        _logger.error("Branch name cannot be empty.")
        raise Exception("Branch name cannot be empty.")

    _run(["push", "origin", branch])


def existsRemoteBranch(name: str):
    out = remoteBranches()
    _logger.info(out)
    gitPipe = subprocess.Popen(["git", "branch", "-r"], stdout=subprocess.PIPE)
    grepPipe = subprocess.Popen(
       ["grep", f"origin/{name}"],
       stdin=gitPipe.stdout,
       stdout=subprocess.PIPE,
       text=True,
    )
    gitPipe.stdout.close()
    output, _ = grepPipe.communicate()

    _logger.info(output)

    return output.strip() == f'origin/{name}'


def remoteBranches():
    _run(["branch", "-r"])


def _run(args: list[str]):
    cmd = ["git"]
    cmd.extend(args)
    _logger.info(" ".join(cmd))

    process = subprocess.run(cmd, capture_output=True, text=True)
    returncode = process.returncode

    if returncode != 0:
        _logger.error(f"Non zero execution result. {returncode}")
        raise Exception(f"Non zero execution result. {returncode}")
    return process.stdout
