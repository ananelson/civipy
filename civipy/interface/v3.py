import json
import subprocess
import urllib3
from civipy.base.config import SETTINGS, logger
from civipy.exceptions import CiviAPIError, CiviHTTPError, CiviProgrammingError
from civipy.interface.base import CiviValue, CiviV3Response, BaseInterface


class V3Interface(BaseInterface):
    __doc__ = (
        BaseInterface.__doc__
        + """
This is the v3 API interface."""
    )

    def __call__(self, action: str, entity: str, params: CiviValue) -> CiviV3Response:
        if self.func is None:
            if SETTINGS.api_version != "3":
                raise CiviProgrammingError(f"API version '{SETTINGS.api_version}' cannot use V3Interface")
            if SETTINGS.api_type == "http":
                self.func = self.http_request
            elif SETTINGS.api_type in ("drush", "wp"):
                self.func = self.run_drush_or_wp_process
            elif SETTINGS.api_type == "cvcli":
                self.func = self.run_cv_cli_process
            else:
                raise CiviProgrammingError(f"API type '{SETTINGS.api_type}' not implemented")
        return self.func(action, entity, params)

    def http_request(self, action: str, entity: str, kwargs: CiviValue) -> CiviV3Response:
        # v3 see https://docs.civicrm.org/dev/en/latest/api/v3/rest/
        params = self._params(entity, action, kwargs)

        # header for v3 API per https://docs.civicrm.org/dev/en/latest/api/v3/rest/#x-requested-with
        headers = {"X-Requested-With": "XMLHttpRequest"}

        # v3 API GET actions apparently all start with "get"; POST actions are create, delete, etc.
        method = "GET" if action.startswith("get") else "POST"
        # urllib3 uses the `fields` parameter to compose the query string for GET requests,
        # and uses the same parameter to compose form data for POST requests
        response = urllib3.request(method, SETTINGS.rest_base, fields=params, headers=headers)
        return self.process_http_response(response)

    @staticmethod
    def _params(entity: str, action: str, kwargs: CiviValue) -> CiviValue:
        params = {
            "entity": entity,
            "action": action,
            "api_key": SETTINGS.user_key,
            "debug": 1,
            "key": SETTINGS.site_key,
            "json": 1,
            "sequential": 1,
        }
        if kwargs:
            for key, value in kwargs.items():
                if value is None:
                    continue
                params[key] = value
        return params

    def process_http_response(self, response: urllib3.BaseHTTPResponse) -> CiviV3Response:
        logger.debug(response.url)
        if response.status == 200:
            return self.process_json_response(response.json())
        else:
            raise CiviHTTPError(response)

    def run_cv_cli_process(self, action: str, entity: str, params: CiviValue) -> CiviV3Response:
        # cli.php -e entity -a action [-u user] [-s site] [--output|--json] [PARAMS]
        params = ["--%s=%s" % (k, v) for k, v in params.items()]
        process = subprocess.run(
            [SETTINGS.rest_base, "-e", entity, "-a", action, "--json"] + params, capture_output=True
        )
        return self.process_json_response(json.loads(process.stdout.decode("UTF-8")))

    def run_drush_or_wp_process(self, action: str, entity: str, params: CiviValue) -> CiviV3Response:
        process = subprocess.run(
            [SETTINGS.rest_base, "civicrm-api", "--out=json", "--in=json", "%s.%s" % (entity, action)],
            capture_output=True,
            input=json.dumps(params).encode("UTF-8"),
        )
        return self.process_json_response(json.loads(process.stdout.decode("UTF-8")))

    @staticmethod
    def process_json_response(data: CiviV3Response) -> CiviV3Response:
        if "is_error" in data and data["is_error"] == 1:
            raise CiviAPIError(data)
        return data

    @staticmethod
    def limit(value: int) -> CiviValue:
        return {"options": '{"limit":' + str(value) + "}"}

    @staticmethod
    def where(kwargs: CiviValue) -> CiviValue:
        return kwargs

    @staticmethod
    def values(kwargs: CiviValue) -> CiviValue:
        return kwargs


v3_interface = V3Interface()
__all__ = ["v3_interface"]
