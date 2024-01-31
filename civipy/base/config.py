import logging
import os
import pathlib
import sys
from typing import Callable, Literal
from civipy.exceptions import CiviProgrammingError

try:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib
except ImportError:
    tomllib = None


class Settings:
    def __init__(self):
        self.values: dict[str, Setting] = {
            "rest_base": Setting(required=True),
            "user_key": Setting(required=True, private=True),
            "site_key": Setting(required=lambda: self.values["api_version"].value == "3", private=True),
            "log_file": Setting(),
            "log_level": Setting(default="DEBUG"),
            "api_version": Setting(default="4"),
        }
        self._api_type: Literal["http", "drush", "wp", "cvcli"] | None = None

    def init(self, **kwargs) -> None:
        """set configuration settings then set up logging"""
        for key, value in kwargs.items():
            if key not in self.values:
                continue
            self.values[key].value = value

        # set unset values to default or raise error if they are required
        missing = []
        for key, setting in self.values.items():
            if setting.required and (setting.not_set or not setting.value):
                missing.append(key)
            elif setting.not_set:
                self.values[key].value = None
        if missing:
            raise CiviProgrammingError(f"Missing required configuration values: {missing}")

        # set up logging - if log_file was not set, it will be None and basicConfig will ignore it and set up stream
        logging.basicConfig(filename=self.values["log_file"].value, level=self.values["log_level"].value)

    @property
    def api_type(self) -> str:
        if self._api_type is None:
            self._read_config()
            # determine value for api_type
            base = self.rest_base.lower()
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
        env_values = {key[5:].lower(): value for key, value in os.environ.items() if key.startswith("CIVI_")}
        if env_values:
            source = " and ".join(filter(None, (source, "environment variables")))
            values.update(env_values)
        self.init(**values)
        logger.debug("CiviPy settings read from %s", source)

    def __getattr__(self, item: str):
        """Look up config value, with fallback to read environment variables or config files"""
        if item not in self.values:
            return super().__getattribute__(item)
        if self.values[item].not_set:
            self._read_config()
        return self.values[item].value

    def __repr__(self):
        values = []
        for k, v in self.values.items():
            if v.not_set:
                value = "[UNSET]"
            elif v.value is None:
                value = "None"
            elif v.private:
                value = "[SET]"
            else:
                value = f"'{v.value}'"
            values.append(f"{k}={value}")
        return f"<Settings {' '.join(values)}>"


class Setting:
    def __init__(self, default: str | None = None, required: bool | Callable[[], bool] = False, private: bool = False):
        self.not_set = True
        self.private = private
        self._is_required = required
        self._default = default
        self._value: str | None = None

    @property
    def required(self) -> bool:
        return self._is_required() if callable(self._is_required) else self._is_required

    @property
    def value(self) -> str | None:
        return None if self.not_set else self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        self.not_set = False
        self._value = self._default if new_value is None else new_value

    def __repr__(self):
        return self.value or ""


def read_dot_civipy(file: pathlib.Path) -> dict[str, str | None]:
    """read settings from .civipy file"""
    values = {}
    with file.open() as fp:
        for line in fp:
            if line.startswith("#"):
                continue
            key, _, line_value = line.partition("=")
            value, _, comment = line_value.partition(" #")
            values[key.lower().strip()] = value.strip() or None
    return values


def read_pyproject_toml(file: pathlib.Path) -> dict[str, str | None]:
    """read settings from pyproject.toml file"""
    if tomllib is None:
        return {}
    with open(file, "rb") as fp:
        pyproject_toml = tomllib.load(fp)
    config = pyproject_toml.get("tool", {}).get("civipy", {})
    return {key.replace("-", "_"): value or None for key, value in config.items()}


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


SETTINGS = Settings()
logger = logging.getLogger("civipy")
__all__ = ["SETTINGS", "logger"]
