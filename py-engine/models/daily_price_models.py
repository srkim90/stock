import gzip
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Union
from marshmallow import fields
from dataclasses_json import dataclass_json, config

from common.define import DATA_PATH, DAY_PRICE


@dataclass_json
@dataclass
class DailyPrice:
    code: str
    period: str  # D, W, M (일/주/월)
    stck_bsop_date: datetime = field(  # 주식 영업 일자 ex> "20230203",
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    stck_oprc: int  # 주식 시가 ex> "179",
    stck_hgpr: int  # 주식 최고가 ex> "180",
    stck_lwpr: int  # 주식 최저가 ex> "177",
    stck_clpr: int  # 주식 종가 ex> "178",
    acml_vol: int  # 누적 거래량 ex> "1047733",
    prdy_vrss_vol_rate: float  # 전일 대비 거래량 비율 ex> "-65.79",
    prdy_vrss: int  # 전일 대비 ex> "-1",
    prdy_vrss_sign: int  # 전일 대비 부호 ex> "5",
    prdy_ctrt: float  # 전일 대비율 ex> "-0.56",
    hts_frgn_ehrt: float  # HTS 외국인 소진율 ex> "0.00",
    frgn_ntby_qty: int  # 외국인 순매수 수량 ex> "0",
    flng_cls_code: str  # 락 구분 코드 ex> "00",
    acml_prtt_rate: float  # 누적 분할 비율 ex> "1.00"


def build_daily_price(code: str, period: str, data: dict) -> DailyPrice:
    return DailyPrice(code=code,
                      period=period,
                      stck_bsop_date=datetime.strptime(data["stck_bsop_date"], "%Y%m%d"),
                      stck_oprc=int(data["stck_oprc"]),
                      stck_hgpr=int(data["stck_hgpr"]),
                      stck_lwpr=int(data["stck_lwpr"]),
                      stck_clpr=int(data["stck_clpr"]),
                      acml_vol=int(data["acml_vol"]),
                      prdy_vrss_vol_rate=float(data["prdy_vrss_vol_rate"]),
                      prdy_vrss=int(data["prdy_vrss"]),
                      prdy_vrss_sign=int(data["prdy_vrss_sign"]),
                      prdy_ctrt=float(data["prdy_ctrt"]),
                      hts_frgn_ehrt=float(data["hts_frgn_ehrt"]),
                      frgn_ntby_qty=int(data["frgn_ntby_qty"]),
                      flng_cls_code=data["flng_cls_code"],
                      acml_prtt_rate=float(data["acml_prtt_rate"]))


@dataclass_json
@dataclass
class DailyPriceAll:
    def __init__(self) -> None:
        super().__init__()
        self.items = []
        self.codes = []
        self.code_dict = {}

    items: List[DailyPrice]

    # refresh 수행 시 자동 생설
    codes: List[str]
    code_dict: Dict[str, DailyPrice]

    def refresh(self):
        self.codes = []
        self.code_dict = {}
        for item in self.items:
            self.codes.append(item.code)
            self.code_dict[item.code] = item


def load_day_price_all(f_name: str) -> DailyPriceAll:
    # if f_name is None:
    #     save_path = os.path.join(DATA_PATH, DAY_PRICE)
    if ".gz" in f_name:
        fd = gzip.open(f_name, "rb")
    else:
        fd = open(f_name, "rb")
    data = fd.read()
    fd.close()
    data_obj: DailyPriceAll = DailyPriceAll()
    for item in json.loads(data):
        data_obj.items.append(DailyPrice.from_dict(item))
    data_obj.items.reverse()
    data_obj.refresh()
    return data_obj
