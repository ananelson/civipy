import logging
import os
import pathlib

logger = logging.getLogger("civipy")
NOTSET = object()
REQUIRED = ["rest_base", "user_key", "site_key"]
OPTIONAL = ["log_file", "log_level"]
ALL_KEYS = ["api_type"] + REQUIRED + OPTIONAL


class Settings:
    def __init__(self):
        self.__dict__.update({key: NOTSET for key in ALL_KEYS})

    def from_environment(self):
        # load credentials from OS environment
        values = {}
        for key in REQUIRED + OPTIONAL:
            values[key] = os.environ.get(f"CIVI_{key.upper()}") or os.environ.get(f"CIVIPY_{key.upper()}")
        if not values["rest_base"]:
            values["rest_base"] = os.environ.get('CIVI_API_BASE')
        missing = [f"CIVI_{key.upper()}" for key in REQUIRED if not values[key]]
        if missing:
            raise Exception(f"Environment missing required configuration values: {missing}")
        self._post_read(values)
        logger.info("Loaded configuration from environment")

    def from_file(self, file):
        # load credentials from file
        if isinstance(file, str):
            file = pathlib.Path(file)
        if hasattr(file, "readlines"):
            values = self._read_file(file)
        elif not hasattr(file, "open"):
            with open(file) as fp:
                values = self._read_file(fp)
        else:
            with file.open() as fp:
                values = self._read_file(fp)
        missing = [key for key in REQUIRED if not values[key]]
        if missing:
            raise Exception(f"Config file {file} missing required configuration values: {missing}")
        self._post_read(values)
        logger.info("Loaded configuration from file %s", file)

    def _read_file(self, file):
        values = {}
        for line in file:
            key, *value = line.split("=", 1)
            if len(value) == 0:
                continue
            key = f"_{key.lower.strip()}"
            value = value[0].strip()
            if not hasattr(self, key):
                continue
            values[key] = value
        return values

    def from_caller(self, **kwargs):
        missing = [key for key in REQUIRED if not kwargs.get(key)]
        if missing:
            raise Exception(f"Missing required configuration values: {missing}")
        values = {key: value for key, value in kwargs.items() if key in ALL_KEYS}
        self._post_read(values)
        logger.info("Loaded configuration from caller")

    def _post_read(self, values):
        # determine value for api_type
        if 'http' in values["rest_base"]:
            values["api_type"] = 'http'
        elif 'drush' in values["rest_base"]:
            values["api_type"] = 'drush'
        else:
            values["api_type"] = 'cvcli'
        for key in ALL_KEYS:
            if key not in values:
                values[key] = None
        self.__dict__.update(values)

        # set up logging
        if self._log_level:
            logger.setLevel(self._log_level)
        if self._log_file:
            h = logging.FileHandler(self._log_file)
            h.setLevel(self._log_level or logging.DEBUG)
            logger.addHandler(h)

    def __getattribute__(self, item: str):
        """Look up config value, with fallback to read environment variables"""
        if item in ALL_KEYS:
            if self.__dict__[item] is NOTSET:
                self.from_environment()
            return Settings.__dict__[item]
        return super().__getattribute__(item)


logger.setLevel(logging.DEBUG)
SETTINGS = Settings()
