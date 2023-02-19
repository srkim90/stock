from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from marshmallow import fields
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class DailyItemChartPrice:
    code: str
    period: str  # D, W, M (일/주/월)
    stck_bsop_date: datetime = field(  # 주식 영업 일자 ex> "20230203",
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    stck_clpr: int  # "178", 주식 종가
    stck_oprc: int  # "179", 주식 시가
    stck_hgpr: int  # "180", 주식 최고가
    stck_lwpr: int  # "177", 주식 최저가
    acml_vol: int  # "1047733", 누적 거래량
    acml_tr_pbmn: int  # "185855049", 누적 거래 대금
    flng_cls_code: str  # "00", 락 구분 코드
                            # 00:해당사항없음(락이 발생안한 경우)
                            # 01:권리락
                            # 02:배당락
                            # 03:분배락
                            # 04:권배락
                            # 05:중간(분기)배당락
                            # 06:권리중간배당락
                            # 07:권리분기배당락
    prtt_rate: float  # "0.00", 분할 비율
    mod_yn: bool  # "N", 분할변경여부
    prdy_vrss_sign: str  # "5", 전일 대비 부호
    prdy_vrss: str  # "-1", 전일 대비
    revl_issu_reas: str  # "" 재평가사유코드


def build_daily_item_chart_price(code: str, period: str, data: dict) -> DailyItemChartPrice:
    return DailyItemChartPrice(code=code,
                               period=period,
                               stck_bsop_date=datetime.strptime(data["stck_bsop_date"], "%Y%m%d"),
                               stck_clpr=int(data["stck_clpr"]),
                               stck_oprc=int(data["stck_oprc"]),
                               stck_hgpr=int(data["stck_hgpr"]),
                               stck_lwpr=int(data["stck_lwpr"]),
                               acml_vol=int(data["acml_vol"]),
                               acml_tr_pbmn=int(data["acml_tr_pbmn"]),
                               flng_cls_code=data["flng_cls_code"],
                               prtt_rate=float(data["prtt_rate"]),
                               mod_yn=True if data["mod_yn"] == "Y" else False,
                               prdy_vrss_sign=data["prdy_vrss_sign"],
                               prdy_vrss=data["prdy_vrss"],
                               revl_issu_reas=data["revl_issu_reas"])


@dataclass_json
@dataclass
class DailyItemChartPriceAll:
    def __init__(self) -> None:
        super().__init__()
        self.items = []
        self.codes = []
        self.code_dict = {}

    items: List[DailyItemChartPrice]

    # refresh 수행 시 자동 생설
    codes: List[str]
    code_dict: Dict[str, DailyItemChartPrice]

    def refresh(self):
        self.codes = []
        self.code_dict = {}
        for item in self.items:
            self.codes.append(item.code)
            self.code_dict[item.code] = item
