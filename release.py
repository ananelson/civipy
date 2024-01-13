#!/usr/bin/python3
from pathlib import Path
from subprocess import run
from sys import argv, stderr, exit


def process_command() -> None:
    """Read the command line arguments and branch accordingly."""
    file = Path(argv[0]).with_name("VERSION")
    level: int | None = None
    for cmd in argv[1:]:
        cmd = cmd.lower().lstrip("-")
        if cmd == "major":
            level = 0
            continue
        if cmd == "minor":
            level = 1
            continue
        if cmd == "patch":
            level = 2
            continue
        if cmd in ("h", "help"):
            print_usage()
            exit(0)
        if cmd in ("v", "version"):
            if file.is_file():
                print(f"CiviPy Version {file.read_text()}")
                exit(0)
            print("ERROR: release.py must be in the root directory of the CiviPy repo.", file=stderr)
            exit(1)
    if level is None:
        print("ERROR: invalid command line arguments. Try 'release.py --help' for more information.", file=stderr)
        exit(1)
    tag = update_version(file, level)
    release(tag)


def print_usage() -> None:
    """Print a usage message for this script."""
    print("""usage: release.py (major|minor|patch)
       release.py -v | --version
       release.py -h | --help
Increments the version number at the specified level and issues a release to PyPI.

Examples:
  release.py minor       If current version is 1.1.1, updates version to 1.2.0 and issues a release.
  release.py --version   Print the current version and exit.
  release.py --help      Print this help message and exit.
""")


def update_version(version_file: Path, level: int) -> str:
    """Increment the package version in the VERSION file at the specified level."""
    # get version elements as ints (e.g. [0, 0, 1])
    version_parts = [int(v) for v in version_file.read_text().strip().split(".")]
    # increment selected level
    version_parts[level] += 1
    for lower in range(level + 1, 3):
        version_parts[lower] = 0
    # save new version number
    new_version = ".".join(map(str, version_parts))
    version_file.write_text(new_version)
    return new_version


def release(tag: str) -> None:
    """Create a release with the version `tag`."""
    root = Path(argv[0]).parent
    # commit change to version number
    run(["git", "add", "VERSION"], cwd=root)
    run(["git", "commit", "-m", f"release ${tag}"], cwd=root)
    # tag and push to GitHub for GitHub Actions to publish
    run(["git", "tag", tag], cwd=root)
    run(["git", "push", "origin", tag], cwd=root)


if __name__ == "__main__":
    process_command()
