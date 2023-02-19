import base64
import json
import os
from typing import Union, Tuple

import requests

from common.define import KEY_STORE_PATH, OPEN_API_BASE_URL
from common.utils import make_url


class AccessTokenProvider:
    APP_KEY: str
    APP_SECRET: str

    def __init__(self) -> None:
        self.KEY_STORE = KEY_STORE_PATH
        self.ACCESS_TOKEN_STORE_PATH = "key.pem"
        self.APP_KEY, self.APP_SECRET = self.__load_app_key_pair()
        self.ACCESS_TOKEN = self.__make_access_token()
        super().__init__()

    def get_access_token(self):
        return self.ACCESS_TOKEN

    def refresh_token(self):
        self.__make_access_token(is_refresh=True)
        return self.get_access_token()

    def http_auth_header(self, token=None):
        if token is None:
            token = self.ACCESS_TOKEN
        return {"Content-Type": "application/json",
                "Authorization": "Bearer %s" % token,
                "AppKey": self.APP_KEY,
                "AppSecret": self.APP_SECRET}

    def __check(self, token=None) -> bool:
        path = "uapi/domestic-stock/v1/quotations/inquire-price"
        headers = self.http_auth_header(token)
        headers["tr_id"] = "FHKST01010100"
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": "005930"
        }
        res = requests.get(make_url(path), headers=headers, params=params)
        if res.status_code == 200:
            return True
        return False

    def __load_app_key_pair(self) -> Tuple[str, str]:
        key_store = os.path.join(self.KEY_STORE, "key_pair.json")
        if os.path.exists(key_store) is False:
            raise FileNotFoundError
        with open(key_store, "rb") as fd:
            pair = json.loads(fd.read())
        key = base64.b64decode(pair["key"].encode()).decode("utf-8")
        secret = base64.b64decode(pair["secret"].encode()).decode("utf-8")
        return key, secret

    def __load_access_token(self) -> Union[str, None]:
        store_path = os.path.join(self.KEY_STORE, self.ACCESS_TOKEN_STORE_PATH)
        if os.path.exists(store_path) is False:
            return None
        with open(store_path, "rb") as fd:
            token = fd.read().strip().decode("utf-8").replace("\n", "").replace("\t", "").replace(" ", "")
        if len(token) < 300 or len(token) > 400:
            return None
        return token

    def __save_access_token(self, token: str) -> None:
        store_path = os.path.join(self.KEY_STORE, self.ACCESS_TOKEN_STORE_PATH)
        with open(store_path, "wb") as fd:
            fd.write(token.encode("utf-8"))

    def __check_access_token(self) -> Union[str, None]:
        token = self.__load_access_token()
        if self.__check(token) is True:
            return token
        return None



    def __make_access_token(self, is_refresh=False):
        if is_refresh is False:
            token = self.__check_access_token()
            if token is not None:
                return token
        headers = {"content-type": "application/json"}
        body = {"grant_type": "client_credentials",
                "appkey": self.APP_KEY,
                "appsecret": self.APP_SECRET}
        res = requests.post(make_url("oauth2/tokenP"), headers=headers, data=json.dumps(body))
        if res.status_code != 200:
            raise Exception
        token = res.json()["access_token"]
        self.__save_access_token(token)
        return token

    def __make_api_header(self):
        return


access_token_provider: AccessTokenProvider = None


def access_token_init():
    global access_token_provider
    if access_token_provider is None:
        access_token_provider = AccessTokenProvider()


def get_access_token():
    access_token_init()
    return access_token_provider.get_access_token()


def refresh_token():
    access_token_init()
    return access_token_provider.refresh_token()


def http_auth_header():
    access_token_init()
    return access_token_provider.http_auth_header()
