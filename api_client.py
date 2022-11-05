import requests
from urllib.parse import urljoin
import json
import sys
import logging

from urllib3.exceptions import InsecureRequestWarning

logger = logging.getLogger(__name__)
logger.info("running %s" % " ".join(sys.argv))


class APIClient:

    default_headers = {
        "User-Agent": "&quot;&quot;Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36&quot;",
    }

    def __init__(
        self,
        base_url
    ):
        self._api_base_url = base_url
        self._session = requests.Session()
        self._session.headers.update(self.default_headers)
        self._ssl_check = False
        self.ssl_verification_check()

    def get(
        self, path: str, params: dict = None, data=None, headers: dict = None
    ) -> requests.Response:
        """Get request"""
        return self._call("GET", path, params=params, data=data, headers=headers)

    def _call(self, method, path, params: dict = None, data=None, headers: dict = None):

        if str(method).upper() not in ("GET", "POST", "PUT", "DELETE", "PATCH"):
            raise ValueError("invalid method <{0}>".format(method))
        url = urljoin(self._api_base_url, path)
        self.set_headers(headers)
        try:
            resp = self._session.request(
                method,
                url,
                params=params,
                data=json.dumps(data),
                verify=self._ssl_check,
            )
            return resp
        except ConnectionError:
            logger.warning("Connection error")

    def set_headers(self, headers):
        """Set headers to _session"""
        if headers is not None and isinstance(headers, dict):
            self._session.headers.update(headers)

    def ssl_verification_check(self):
        if not self._ssl_check:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

