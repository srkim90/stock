from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Union
from marshmallow import fields
from dataclasses_json import dataclass_json, config

from models.base_model_all import BaseModelAll

''' StockMst2
0  - (string) 종목 코드
1  - (string) 종목명
2  - (long) 시간(HHMM)
3  - (long) 현재가
4  - (long) 전일대비
5  - (char) 상태구분
6  - (long) 시가
7  - (long) 고가
8  - (long) 저가
9  - (long) 매도호가
10 - (long) 매수호가
11 - (unsigned long) 거래량 [주의] 단위 1주
12 - (long) 거래대금 [주의] 단위 천원
13 - (long) 총매도잔량
14 - (long) 총매수잔량
15 - (long) 매도잔량
16 - (long) 매수잔량
17 - (unsigned long) 상장주식수
18 - (long) 외국인보유비율(%)
19 - (long) 전일종가
20 - (unsigned long) 전일거래량
21 - (long) 체결강도
22 - (unsigned long) 순간체결량
23 - (char) 체결가비교 Flag
24 - (char) 호가비교 Flag
25 - (char) 동시호가구분
26 - (long) 예상체결가
27 - (long) 예상체결가 전일대비
28 - (long) 예상체결가 상태구분
29 - (unsigned long) 예상체결가 거래량
'''


@dataclass_json
@dataclass
class StockMst2Models:
    code: str  # 0  - (string) 종목 코드
    name: str  # 1  - (string) 종목명
    actual_time: datetime = field(  # 2  - (long) 시간(HHMM), 받을땐 hhmm인데 내부적으로 datetime으로 변환을 해서 넣음
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    data_received_time: datetime = field(  # X  - 수신 시간
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    price: int  # 3  - (long) 현재가
    전일대비: int  # 4  - (long) 전일대비
    상태구분: str  # 5  - (char) 상태구분
    시가: int  # 6  - (long) 시가
    고가: int  # 7  - (long) 고가
    저가: int  # 8  - (long) 저가
    매도호가: int  # 9  - (long) 매도호가
    매수호가: int  # 10 - (long) 매수호가
    거래량: int  # 11 - (unsigned long) 거래량 [주의] 단위 1주
    거래대금: int  # 12 - (long) 거래대금 [주의] 단위 천원
    총매도잔량: int  # 13 - (long) 총매도잔량
    총매수잔량: int  # 14 - (long) 총매수잔량
    매도잔량: int  # 15 - (long) 매도잔량
    매수잔량: int  # 16 - (long) 매수잔량
    상장주식수: int  # 17 - (unsigned long) 상장주식수
    외국인보유비율: int  # 18 - (long) 외국인보유비율(%)
    전일종가: int  # 19 - (long) 전일종가
    전일거래량: int  # 20 - (unsigned long) 전일거래량
    체결강도: int  # 21 - (long) 체결강도
    순간체결량: int  # 22 - (unsigned long) 순간체결량
    체결가비교: str  # 23 - (char) 체결가비교 Flag
    호가비교: str  # 24 - (char) 호가비교 Flag
    동시호가구분: str  # 25 - (char) 동시호가구분
    예상체결가: int  # 26 - (long) 예상체결가
    예상체결가_전일대비: int  # 27 - (long) 예상체결가 전일대비
    예상체결가_상태구분: int  # 28 - (long) 예상체결가 상태구분
    예상체결가_거래량: int  # 29 - (unsigned long) 예상체결가 거래량

    def make_redis_key(self, now_time: datetime, bz_yyyymmdd: str):
        return self.static_make_redis_key(self.code, now_time, bz_yyyymmdd)

    @staticmethod
    def static_make_redis_key(code: str, now_time: datetime, bz_yyyymmdd: str):
        return "%s.%s.%s" % (bz_yyyymmdd, now_time.strftime("%H%M%S"), code)


@dataclass_json
@dataclass
class StockMst2ModelsAll(BaseModelAll):
    items: List[StockMst2Models]

    def __init__(self) -> None:
        super().__init__()

    def add(self, data: StockMst2Models) -> None:
        super(StockMst2ModelsAll, self).add(data)
        return
