from dataclasses import dataclass, field
import datetime
from typing import List, Dict, Union
from marshmallow import fields
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Holiday:
    def __lt__(self, other):
        return self.bass_dt < other.bass_dt

    def __le__(self, other):
        return self.bass_dt <= other.bass_dt

    def __gt__(self, other):
        return self.bass_dt > other.bass_dt

    def __ge__(self, other):
        return self.bass_dt >= other.bass_dt

    def __eq__(self, other):
        return self.bass_dt == other.bass_dt

    def __ne__(self, other):
        return self.bass_dt != other.bass_dt

    bass_dt: datetime = field(  # 기준일자 ex> "20230203",
        metadata=config(
            encoder=datetime.datetime.isoformat,
            decoder=datetime.datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    wday_dvsn_cd: str  # 요일구분코드, 01:토요일 02:일요일, 03:월요일 ~ 07:금요일
    bzdy_yn: bool  # 영업일여부,
    tr_day_yn: bool  # 거래일여부,
    opnd_yn: bool  # 개장일여부,
    sttl_day_yn: bool  # 결제일여부,


def build_holiday(data: dict) -> Holiday:
    return Holiday(bass_dt=datetime.datetime.strptime(data["bass_dt"], "%Y%m%d"),
                   wday_dvsn_cd=data["wday_dvsn_cd"],
                   bzdy_yn=True if "Y" == data["bzdy_yn"] else False,
                   tr_day_yn=True if "Y" == data["tr_day_yn"] else False,
                   opnd_yn=True if "Y" == data["opnd_yn"] else False,
                   sttl_day_yn=True if "Y" == data["sttl_day_yn"] else False)


@dataclass_json
@dataclass
class HolidayAll:
    def __init__(self, items=None) -> None:
        super().__init__()
        if items is None:
            self.items = []
        else:
            self.items = items
        self.yyyymmdd_list = []
        self.yymmdd_dict = {}

    items: List[Holiday]

    # refresh 수행 시 자동 생설
    yyyymmdd_list: List[str]
    yymmdd_dict: Dict[str, Holiday]

    def get_last_bz_day(self, base_yyyymmdd=None) -> datetime.datetime:
        if base_yyyymmdd is None:
            n_day_ago = 0
            now_time = datetime.datetime.now()
            if (datetime.datetime.now().hour * 60) + now_time.minute < 330:
                n_day_ago = 1
            base_date = datetime.date.today() - datetime.timedelta(n_day_ago)
        else:
            base_date = datetime.datetime.strptime(base_yyyymmdd, "%Y%m%d")
        for idx in range(10):
            check_date = (base_date - datetime.timedelta(idx))
            check_yyyymmdd = check_date.strftime("%Y%m%d")
            holiday: Holiday = self.yymmdd_dict[check_yyyymmdd]
            if holiday.bzdy_yn is True:
                return check_date
        raise FileNotFoundError

    def get_last_bz_day_str(self, base_yyyymmdd=None) -> str:
        return self.get_last_bz_day(base_yyyymmdd).strftime("%Y%m%d")

    def refresh(self):
        self.yyyymmdd_list = []
        self.yymmdd_dict = {}
        for item in self.items:
            yyyymmdd = item.bass_dt.strftime("%Y%m%d")
            self.yyyymmdd_list.append(yyyymmdd)
            self.yymmdd_dict[yyyymmdd] = item
        self.items.sort()

    def is_holiday(self, yyyymmdd: Union[str, datetime.datetime]) -> bool:
        if type(yyyymmdd) == datetime:
            yyyymmdd = yyyymmdd.strftime("%Y%m%d")
        try:
            item = self.yymmdd_dict[yyyymmdd]
        except KeyError:
            return True
        return item.bzdy_yn


def merge_holiday(dst: HolidayAll, src: HolidayAll) -> None:
    dst.refresh()
    src.refresh()
    for yyyymmdd in src.yyyymmdd_list:
        if yyyymmdd not in dst.yyyymmdd_list:
            dst.items.append(src.yymmdd_dict[yyyymmdd])
        else:
            check_idx = None
            for idx, holiday_at in enumerate(dst.items):
                if yyyymmdd == holiday_at.bass_dt.strftime("%Y%m%d"):
                    check_idx = idx
                    break
            if check_idx is not None:
                del dst.items[check_idx]
    dst.refresh()
