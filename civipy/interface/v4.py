import json
import subprocess
from urllib.parse import urljoin, urlencode
import urllib3
from civipy.base.config import SETTINGS, logger
from civipy.exceptions import CiviAPIError, CiviHTTPError, CiviProgrammingError
from civipy.interface.base import CiviValue, CiviV4Response, BaseInterface, CiviV4Request


class V4Interface(BaseInterface):
    __doc__ = (
        BaseInterface.__doc__
        + """
This is the v4 API interface."""
    )

    def __call__(self, action: str, entity: str, params: CiviV4Request) -> CiviV4Response:
        if self.func is None:
            if SETTINGS.api_version != "4":
                raise CiviProgrammingError(f"API version '{SETTINGS.api_version}' cannot use V4Interface")
            if SETTINGS.api_type == "http":
                self.func = self.http_request
            elif SETTINGS.api_type == "drush":
                self.func = self.run_drush_process
            # API v4 not available to wp-cli - see https://docs.civicrm.org/dev/en/latest/api/v4/usage/#wp-cli
            elif SETTINGS.api_type == "cvcli":
                self.func = self.run_cv_cli_process
            else:
                raise CiviProgrammingError(f"API type '{SETTINGS.api_type}' not implemented")
        return self.func(action, entity, params)

    def http_request(self, action: str, entity: str, kwargs: CiviV4Request) -> CiviV4Response:
        # v4 see https://docs.civicrm.org/dev/en/latest/api/v4/rest/
        url = urljoin(SETTINGS.rest_base, "/".join((entity, action)))
        body = urlencode({"params": json.dumps(kwargs, separators=(",", ":"))})
        logger.debug("Request for %s: %s", url, body)

        # header for v4 API per https://docs.civicrm.org/dev/en/latest/api/v4/rest/#x-requested-with
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "X-Civi-Auth": f"Bearer {SETTINGS.user_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # v4 docs: "Requests are typically submitted with HTTP POST, but read-only operations may use HTTP GET."
        response = urllib3.request("POST", url, body=body, headers=headers)
        return self.process_http_response(response)

    def process_http_response(self, response: urllib3.BaseHTTPResponse) -> CiviV4Response:
        logger.debug(response.url)
        if response.status == 200:
            return self.process_json_response(response.json())
        else:
            raise CiviHTTPError(response)

    def run_cv_cli_process(self, action: str, entity: str, params: CiviValue) -> CiviV4Response:
        # see `cv --help api4` or https://docs.civicrm.org/dev/en/latest/api/v4/usage/#cv
        process = subprocess.run(
            [
                SETTINGS.rest_base,
                "api4",
                ".".join((entity, action)),
                json.dumps(params, separators=(",", ":")).encode("UTF-8"),
            ],
            capture_output=True,
        )
        return self.process_json_response(json.loads(process.stdout.decode("UTF-8")))

    def run_drush_process(self, action: str, entity: str, params: CiviValue) -> CiviV4Response:
        process = subprocess.run(
            [SETTINGS.rest_base, "civicrm-api", "version=4", "--out=json", "--in=json", "%s.%s" % (entity, action)],
            capture_output=True,
            input=json.dumps(params, separators=(",", ":")).encode("UTF-8"),
        )
        return self.process_json_response(json.loads(process.stdout.decode("UTF-8")))

    @staticmethod
    def process_json_response(data: CiviV4Response) -> CiviV4Response:
        if "is_error" in data and data["error_code"] > 0:
            raise CiviAPIError(data)
        return data

    @staticmethod
    def limit(value: int) -> CiviV4Request:
        return {"limit": value}

    @staticmethod
    def where(kwargs: CiviValue) -> CiviV4Request:
        return {"where": [[k, "=", v] for k, v in kwargs.items()]}

    @staticmethod
    def values(kwargs: CiviValue) -> CiviV4Request:
        return {"values": kwargs}


v4_interface = V4Interface()
__all__ = ["v4_interface"]
