from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from marshmallow import fields
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class TimeItemChartPrice:
    code: str
    stck_bsop_date: datetime = field(  # 주식 영업 일자 + 주식 체결 시간 : stck_bsop_date + stck_cntg_hour
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    stck_prpr: int  # '173' 주식 현재가
    stck_oprc: int  # '173' 주식 시가2
    stck_hgpr: int  # '173' 주식 최고가
    stck_lwpr: int  # '173' 주식 최저가
    cntg_vol: int  # '81373' 체결 거래량
    acml_tr_pbmn: int  # '295318796' 누적 거래 대금


def build_time_item_chart_price(code: str, data: dict) -> TimeItemChartPrice:
    return TimeItemChartPrice(code=code,
                              stck_bsop_date=datetime.strptime(
                                  "%s_%s" % (data["stck_bsop_date"], data["stck_cntg_hour"]), "%Y%m%d_%H%M%S"),
                              stck_prpr=int(data["stck_prpr"]),
                              stck_oprc=int(data["stck_oprc"]),
                              stck_hgpr=int(data["stck_hgpr"]),
                              stck_lwpr=int(data["stck_lwpr"]),
                              cntg_vol=int(data["cntg_vol"]),
                              acml_tr_pbmn=int(data["acml_tr_pbmn"]))


@dataclass_json
@dataclass
class TimeItemChartPriceAll:
    def __init__(self) -> None:
        super().__init__()
        self.items = []
        self.codes = []
        self.code_dict = {}

    items: List[TimeItemChartPrice]

    # refresh 수행 시 자동 생설
    codes: List[str]
    code_dict: Dict[str, TimeItemChartPrice]

    def refresh(self):
        self.codes = []
        self.code_dict = {}
        for item in self.items:
            self.codes.append(item.code)
            self.code_dict[item.code] = item
