import datetime
from dataclasses import dataclass
from typing import List, Dict, Union

from dataclasses_json import dataclass_json


# 'stck_cntg_hour' = {str} '155525'
# 'stck_prpr' = {str} '2970'
# 'prdy_vrss' = {str} '260'
# 'prdy_vrss_sign' = {str} '2'
# 'prdy_ctrt' = {str} '9.59'
# 'askp' = {str} '2970'
# 'bidp' = {str} '2965'
# 'tday_rltv' = {str} '98.67'
# 'acml_vol' = {str} '29201458'
# 'cnqn' = {str} '20'


@dataclass_json
@dataclass
class TimeItemConclusion:
    code: str  #
    stck_cntg_hour: str  # '155525'
    stck_prpr: int  # '2970'
    prdy_vrss: int  # '260'
    prdy_vrss_sign: str  # '2'
    prdy_ctrt: float  # '9.59'
    askp: int  # '2970'
    bidp: int  # '2965'
    tday_rltv: float  # '98.67'
    acml_vol: int  # '29201458'
    cnqn: int  # '20'


@dataclass_json
@dataclass
class TimeItemConclusionAll:
    items: List[TimeItemConclusion]

    def __init__(self, data_list: List[TimeItemConclusion] = None) -> None:
        super().__init__()
        self.items = []
        if data_list is not None:
            self.items = data_list

    def add(self, items: List[TimeItemConclusion]):
        self.items += items

    def get_last(self) -> Union[None, str]:
        length = len(self.items)
        if length == 0:
            return None
        last_hhmmss = self.items[-1].stck_cntg_hour
        last_date = datetime.datetime.strptime("20000101" + "_" + last_hhmmss, "%Y%m%d_%H%M%S") - datetime.timedelta(
            seconds=1)
        return last_date.strftime("%H%M%S")

    def remove_last(self) -> Union[None, str]:
        length = len(self.items)
        if length == 0:
            return None
        last_hhmmss = self.items[-1].stck_cntg_hour
        n_same = 0
        for idx in range(length):
            check_target = self.items[-1 * (idx + 1)]
            if check_target.stck_cntg_hour == last_hhmmss:
                n_same += 1
                continue
            break
        self.items = self.items[0:n_same * -1]
        return last_hhmmss


def build_time_item_conclusion_all(code: str, data_list: List[dict]) -> TimeItemConclusionAll:
    result_list: List[TimeItemConclusion] = []
    for data in data_list:
        result_list.append(build_time_item_conclusion(code, data))
    return TimeItemConclusionAll(result_list)


def build_time_item_conclusion(code: str, data: dict) -> TimeItemConclusion:
    return TimeItemConclusion(code=code,
                              stck_cntg_hour=data["stck_cntg_hour"],
                              stck_prpr=int(data["stck_prpr"]),
                              prdy_vrss=int(data["prdy_vrss"]),
                              prdy_vrss_sign=data["prdy_vrss_sign"],
                              prdy_ctrt=float(data["prdy_ctrt"]),
                              askp=int(data["askp"]),
                              bidp=int(data["bidp"]),
                              tday_rltv=float(data["tday_rltv"]),
                              acml_vol=int(data["acml_vol"]),
                              cnqn=int(data["cnqn"]),
                              )
