import requests
import base64
import json
import time
import hmac

from urllib.parse import urljoin
from enum import Enum
from typing import Union

from config_utils import ConfigUtils, APIConfig


class RequestMethod(Enum):
    GET: str = 'GET'
    POST: str = 'POST'


class RequestUtils:
    def __init__(self, api_config: APIConfig, config: dict):
        self.api_config: APIConfig = api_config
        self.config: dict = config

    def request(self, method: RequestMethod, uri: str, params: dict = None,
                body: dict = None, headers: dict = None, auth: bool = False) -> Union[dict, None]:
        if params:
            query: str = "&".join(
                ["{}={}".format(k, params[k]) for k in sorted(params.keys())]
            )
        url: str = urljoin(self.api_config.base_url, uri)

        if auth:
            timestamp: str = (
                    str(time.time()).split(".")[0]
                    + "."
                    + str(time.time()).split(".")[1][:3]
            )
            if body:
                body: str = json.dumps(body)
            else:
                body: str = ""
            message: str = str(timestamp) + str.upper(method.value()) + uri + str(body)
            mac: hmac.HMAC = hmac.new(
                bytes(self.api_config.secret_key, encoding="utf-8"),
                bytes(message, encoding="utf-8"),
                digestmod="sha256",
            )
            digest: bytes = mac.digest()
            sign: bytes = base64.b64encode(digest)

            if not headers:
                headers = {}
            headers["Content-Type"] = "application/json"
            headers["OK-ACCESS-KEY"] = self.api_config.api_key
            headers["OK-ACCESS-SIGN"] = sign
            headers["OK-ACCESS-TIMESTAMP"] = str(timestamp)
            headers["OK-ACCESS-PASSPHRASE"] = self.api_config.passphrase

        result: dict = requests.request(method.value(), url, data=body, headers=headers, timeout=10).json()
        if result.get('code') and result.get('code') != '0':
            return None
        return result
