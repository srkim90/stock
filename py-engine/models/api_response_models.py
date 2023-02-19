import json
from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import dataclass_json
from requests.structures import CaseInsensitiveDict


@dataclass_json
@dataclass
class QueryApiResponse:
    status_code: int
    http_header: dict
    rt_cd: int  # 성공 실패 여부, 0 : 성공, 0 이외의 값 : 실패
    msg_cd: str  # 응답 코드
    msg1: str  # 응답메세지
    output: dict  # 이름이 'output'인 API 고유 패이로드
    output1: dict  # 이름이 'output1'인 API 고유 패이로드
    output2: dict  # 이름이 'output2'인 API 고유 패이로드


def build_query_api_response(status_code: int, http_header: dict, text_res: str) -> QueryApiResponse:
    dict_res: dict = json.loads(text_res)
    output = {}
    output1 = {}
    output2 = {}
    if "output" in dict_res.keys():
        output = dict_res["output"]
    if "output1" in dict_res.keys():
        output1 = dict_res["output1"]
    if "output2" in dict_res.keys():
        output2 = dict_res["output2"]
    try:
        rt_cd = int(dict_res["rt_cd"])
    except Exception as e:
        rt_cd = 0
    return QueryApiResponse(status_code=status_code,
                            http_header=http_header,
                            rt_cd=rt_cd,
                            msg_cd=dict_res["msg_cd"],
                            msg1=dict_res["msg1"],
                            output=output,
                            output1=output1,
                            output2=output2)
