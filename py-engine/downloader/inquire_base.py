import gzip
import json
import os
import threading
import time
from typing import Union, Tuple, List

import requests

from common.access_token_provider import get_access_token, http_auth_header
from common.define import DATA_PATH
from common.utils import make_url, sa_log, get_uncompressed_size
from models.api_response_models import build_query_api_response, QueryApiResponse

tps_lock = threading.Semaphore(1)


class InquireBase:
    sub_url: str
    tr_id: str
    sub_type: str

    def __init__(self, tr_id: str, sub_url: str, sub_type: str = None) -> None:
        self.sub_url = sub_url
        self.tr_id = tr_id
        self.sub_type = sub_type
        super().__init__()

    def _get_data_save_dir(self) -> str:
        return os.path.join(DATA_PATH, self.sub_type)

    def __build_request_header(self):
        header_set = http_auth_header()
        return header_set

    def _base_json_request(self, query: Union[dict, None] = None,
                           add_header: Union[dict, None] = None,
                           session: Union[requests.Session, None] = None) -> QueryApiResponse:
        try:
            return self.__base_json_request(query, add_header, session)
        except Exception as e:
            return None

    @staticmethod
    def __check_duplicate(f_name: str, data: bytes) -> bool:
        if os.path.exists(f_name) is False:
            f_name += ".gz"
        if os.path.exists(f_name) is False:
            return False
        if ".gz" in f_name.lower():
            file_length = get_uncompressed_size(f_name)
        else:
            file_length = os.stat(f_name).st_size
        data_length = len(data)
        return file_length == data_length

    def get_item_save_path(self, name: str, sub_type: str, sub_dir: str = None, is_gzip: bool = True) -> str:
        save_path = os.path.join(DATA_PATH, sub_type)
        if sub_dir is not None:
            save_path = os.path.join(save_path, sub_dir)
        f_name = os.path.join(save_path, name)
        if is_gzip is True:
            if ".gz" not in f_name.lower():
                f_name = f_name + ".gz"
        return f_name

    @staticmethod
    def _in_load_data(file_path: str, origin_model_type, is_list: bool = False):
        if os.path.exists(file_path) is False:
            if ".gz" not in file_path:
                file_path += ".gz"
            else:
                sa_log("_in_load_data : not exist file=%s" % file_path)
                raise FileNotFoundError
        if os.path.exists(file_path) is False:
            sa_log("_in_load_data : not exist file=%s" % file_path)
            raise FileNotFoundError
        if ".gz" not in file_path:
            fd = open(file_path, "rb")
        else:
            fd = gzip.open(file_path, "rb")
        if is_list is False:
            data = origin_model_type.from_json(fd.read())
        else:
            data = []
            for sub_data in json.loads(fd.read()):
                data.append(origin_model_type.from_dict(sub_data))
        fd.close()
        return data

    def _make_file_dir_name(self, sub_type: str, sub_dir: Union[str, List[str]] = None,
                            name: Union[str, None] = None) -> str:
        save_path = os.path.join(DATA_PATH, sub_type)
        if sub_dir is not None:
            if type(sub_dir) == str:
                sub_dir = [sub_dir, ]
            for sub_dir_at in sub_dir:
                save_path = os.path.join(save_path, sub_dir_at)
        tps_lock.acquire()
        if os.path.exists(save_path) is False:
            os.makedirs(save_path)
        tps_lock.release()
        if name is not None:
            f_name = os.path.join(save_path, name)
        else:
            f_name = save_path
        return f_name

    def _in_save_data(self, name: str, data: any, sub_type: str, sub_dir: Union[str, List[str]] = None,
                      is_gzip: bool = True,
                      data_type: any = None,
                      allow_overwrite: bool = True) -> None:

        f_name = self._make_file_dir_name(sub_type, sub_dir, name)
        if allow_overwrite is False:
            if os.path.exists(f_name) is True:
                return
        if type(data) == dict or type(data) == list:
            data = json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")
        elif type(data) == str:
            data = data.encode("utf-8")
        elif data_type is not None:
            data = data_type.to_json(data, indent=4, ensure_ascii=False).encode("utf-8")
        if InquireBase.__check_duplicate(f_name, data) is True:
            return
        if is_gzip is True:
            if ".gz" not in f_name.lower():
                f_name = f_name + ".gz"
            fd = gzip.open(f_name, "wb")
        else:
            fd = open(f_name, "wb")
        fd.write(data)
        fd.close()
        return

    def __base_json_request(self, query: Union[dict, None] = None,
                            add_header: Union[dict, None] = None,
                            session: Union[requests.Session, None] = None) -> QueryApiResponse:
        status_code, headers, text = self.__base_request(query, add_header, session)
        query_res = build_query_api_response(status_code, headers, text)
        if query_res.rt_cd != 0:
            sa_log("Error. fail to call API : sub_url=%s, tr_id=%s, rt_cd=%s, msg_cd=%s, msg1=%s"
                   % (self.sub_url, self.tr_id, query_res.rt_cd, query_res.msg_cd, query_res.msg1,))
            raise Exception
        return query_res

    def __tps_check(self):
        time.sleep(0.05)

    def __base_request(self, query: Union[dict, None] = None,
                       add_header: Union[dict, None] = None,
                       session: Union[requests.Session, None] = None) -> Tuple[
        int, dict, str]:
        add_header = add_header if add_header is not None else {}
        header_set = self.__build_request_header()
        header_set["tr_id"] = self.tr_id
        for header_item in add_header.keys():
            header_set[header_item] = add_header[header_item]
        self.__tps_check()
        if session is None:
            res = requests.get(make_url(self.sub_url), headers=header_set, params=query)
        else:
            res = session.get(make_url(self.sub_url), headers=header_set, params=query)
        if res.status_code > 299:
            sa_log("Error. fail to call API : sub_url=%s, tr_id=%s, status_code=%d"
                   % (self.sub_url, self.tr_id, res.status_code))
            time.sleep(2.5)
            raise Exception
        return res.status_code, dict(res.headers), res.text
