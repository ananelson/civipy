import logging
import os
import pathlib
import sys
from civipy.exceptions import CiviProgrammingError

try:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib
except ImportError:
    tomllib = None


logger = logging.getLogger("civipy")
NOTSET = object()
REQUIRED = ["rest_base", "user_key", "site_key"]
OPTIONAL = ["log_file", "log_level", "api_version"]
ALL_KEYS = REQUIRED + OPTIONAL
DEFAULTS = {"api_version": "4"}


class Settings:
    def __init__(self):
        self.values: dict[str, str | NOTSET | None] = {key: NOTSET for key in ALL_KEYS}
        self._api_type: str | NOTSET = NOTSET

    def init(self, **kwargs) -> None:
        """set configuration settings then set up logging"""
        for key, value in kwargs.items():
            if key not in ALL_KEYS:
                continue
            self.values[key] = value

        # set unset values to default or raise error if they are required
        missing = []
        for key, value in self.values.items():
            if key in REQUIRED and value in (NOTSET, None):
                missing.append(key)
            elif value is NOTSET:
                self.values[key] = DEFAULTS.get(key, None)
        if missing:
            raise CiviProgrammingError(f"Missing required configuration values: {missing}")

        # set up logging
        if self.values["log_level"]:
            logger.setLevel(self.values["log_level"])
        if self.values["log_file"]:
            h = logging.FileHandler(self.values["log_file"])
            h.setLevel(self.values["log_level"] or logging.DEBUG)
            logger.addHandler(h)

    @property
    def api_type(self) -> str:
        if self._api_type is NOTSET:
            self._read_config()
            # determine value for api_type
            base = self.values["rest_base"].lower()
            if "http" in base:
                self._api_type = "http"
            elif "drush" in base:
                self._api_type = "drush"
            elif "wp" in base:
                self._api_type = "wp"
            else:
                self._api_type = "cvcli"
        return self._api_type

    def _read_config(self) -> None:
        """Read configuration from wherever found"""
        values, source = {}, None
        # Read .civipy or pyproject.toml's tool.civipy section.
        file = find_config_file()
        if file is not None:
            if file.name == "pyproject.toml":
                values, source = read_pyproject_toml(file), str(file)
            else:
                values, source = read_dot_civipy(file), str(file)
        # Read any settings set by environment variables
        env_values = read_environment()
        if env_values:
            source = " and ".join(filter(None, (source, "environment variables")))
            values.update(env_values)
        self.init(**values)
        logger.debug("CiviPy settings read from %s", source)

    def __getattr__(self, item: str):
        """Look up config value, with fallback to read environment variables or config files"""
        if item not in ALL_KEYS:
            return super().__getattribute__(item)
        if self.values[item] is NOTSET:
            self._read_config()
        return self.values[item]


def read_environment() -> dict[str, str | None]:
    """read settings from OS environment"""
    values = {}
    for key in ALL_KEYS:
        name = f"CIVI_{key.upper()}"
        value = os.environ.get(name, NOTSET)
        if value is not NOTSET:
            values.update(set_value(key, value, name))
    return values


def read_dot_civipy(file: pathlib.Path) -> dict[str, str | None]:
    """read settings from .civipy file"""
    values = {}
    with file.open() as fp:
        for line in fp:
            key, _, value = line.partition("=")
            values.update(set_value(key, value, file))
    return values


def read_pyproject_toml(file: pathlib.Path) -> dict[str, str | None]:
    """read settings from pyproject.toml file"""
    values = {}
    if tomllib is None:
        return values
    with open(file, "rb") as fp:
        pyproject_toml = tomllib.load(fp)
    config = pyproject_toml.get("tool", {}).get("civipy", {})
    for key, value in config.items():
        values.update(set_value(key, value, file))
    return values


def find_config_file() -> pathlib.Path | None:
    """Find a .civipy or pyproject.toml file. Look in current directory up to
    project root then check user's home directory for .civipy."""
    env_config = os.environ.get("CIVI_CONFIG")
    if env_config:
        directory = pathlib.Path(env_config).resolve()
        if directory.is_file():
            return directory
        dot_civipy = directory / ".civipy"
        if directory.is_dir() and dot_civipy.is_file():
            return dot_civipy
    start = pathlib.Path.cwd().resolve()
    for directory in [start] + list(start.parents):
        dot_civipy = directory / ".civipy"
        if dot_civipy.is_file():
            return dot_civipy
        pyproject = directory / "pyproject.toml"
        if pyproject.is_file():
            return pyproject
        if (directory / ".git").exists():
            break  # a .git folder suggests this is the project root
    dot_civipy = pathlib.Path.home().resolve() / ".civipy"
    if dot_civipy.is_file():
        return dot_civipy
    return None


def set_value(key: str, value: str, source: pathlib.Path | str) -> dict[str, str | None]:
    """return a dict to update settings with a normalized key and value, raise error identifying `source` if invalid"""
    key = key.replace("-", "_").lower().strip()
    if key not in ALL_KEYS:
        return {}
    value = value.strip()
    if not value:
        if value in REQUIRED:
            raise CiviProgrammingError(f"Invalid value for {key} in {source}")
        value = None
    return {key: value}


logger.setLevel(logging.DEBUG)
SETTINGS = Settings()
__all__ = ["SETTINGS", "logger"]
