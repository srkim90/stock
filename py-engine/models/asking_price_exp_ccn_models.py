from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from marshmallow import fields
from dataclasses_json import dataclass_json, config

from models.base_model_all import BaseModelAll


@dataclass_json
@dataclass
class AskBidPrice:
    aspr_acpt_hour: datetime = field(  # 호가 접수 시간 ex> "160000",
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    askp1: int  # ex> 171 매도호가1
    askp2: int  # ex> 172 매도호가2
    askp3: int  # ex> 173 매도호가3
    askp4: int  # ex> 174 매도호가4
    askp5: int  # ex> 175 매도호가5
    askp6: int  # ex> 176 매도호가6
    askp7: int  # ex> 177 매도호가7
    askp8: int  # ex> 178 매도호가8
    askp9: int  # ex> 179 매도호가9
    askp10: int  # ex> 180 매도호가10
    bidp1: int  # ex> 170 매수호가1
    bidp2: int  # ex> 169 매수호가2
    bidp3: int  # ex> 168 매수호가3
    bidp4: int  # ex> 167 매수호가4
    bidp5: int  # ex> 166 매수호가5
    bidp6: int  # ex> 165 매수호가6
    bidp7: int  # ex> 164 매수호가7
    bidp8: int  # ex> 163 매수호가8
    bidp9: int  # ex> 162 매수호가9
    bidp10: int  # ex> 161 매수호가10
    askp_rsqn1: int  # ex> 37690 매도호가 잔량1
    askp_rsqn2: int  # ex> 225465 매도호가 잔량2
    askp_rsqn3: int  # ex> 90180 매도호가 잔량3
    askp_rsqn4: int  # ex> 83160 매도호가 잔량4
    askp_rsqn5: int  # ex> 102743 매도호가 잔량5
    askp_rsqn6: int  # ex> 111120 매도호가 잔량6
    askp_rsqn7: int  # ex> 113592 매도호가 잔량7
    askp_rsqn8: int  # ex> 70400 매도호가 잔량8
    askp_rsqn9: int  # ex> 178626 매도호가 잔량9
    askp_rsqn10: int  # ex> 106758 매도호가 잔량10
    bidp_rsqn1: int  # ex> 3468 매수호가 잔량1
    bidp_rsqn2: int  # ex> 306582 매수호가 잔량2
    bidp_rsqn3: int  # ex> 106059 매수호가 잔량3
    bidp_rsqn4: int  # ex> 137744 매수호가 잔량4
    bidp_rsqn5: int  # ex> 50139 매수호가 잔량5
    bidp_rsqn6: int  # ex> 33792 매수호가 잔량6
    bidp_rsqn7: int  # ex> 36525 매수호가 잔량7
    bidp_rsqn8: int  # ex> 44620 매수호가 잔량8
    bidp_rsqn9: int  # ex> 3430 매수호가 잔량9
    bidp_rsqn10: int  # ex> 19075 매수호가 잔량10
    askp_rsqn_icdc1: int  # ex> 0 매도호가 잔량 증감1
    askp_rsqn_icdc2: int  # ex> 0 매도호가 잔량 증감2
    askp_rsqn_icdc3: int  # ex> 0 매도호가 잔량 증감3
    askp_rsqn_icdc4: int  # ex> 0 매도호가 잔량 증감4
    askp_rsqn_icdc5: int  # ex> 0 매도호가 잔량 증감5
    askp_rsqn_icdc6: int  # ex> 0 매도호가 잔량 증감6
    askp_rsqn_icdc7: int  # ex> 0 매도호가 잔량 증감7
    askp_rsqn_icdc8: int  # ex> 0 매도호가 잔량 증감8
    askp_rsqn_icdc9: int  # ex> 0 매도호가 잔량 증감9
    askp_rsqn_icdc10: int  # ex> 0 매도호가 잔량 증감10
    bidp_rsqn_icdc1: int  # ex> 0 매수호가 잔량 증감1
    bidp_rsqn_icdc2: int  # ex> 0 매수호가 잔량 증감2
    bidp_rsqn_icdc3: int  # ex> 0 매수호가 잔량 증감3
    bidp_rsqn_icdc4: int  # ex> 0 매수호가 잔량 증감4
    bidp_rsqn_icdc5: int  # ex> 0 매수호가 잔량 증감5
    bidp_rsqn_icdc6: int  # ex> 0 매수호가 잔량 증감6
    bidp_rsqn_icdc7: int  # ex> 0 매수호가 잔량 증감7
    bidp_rsqn_icdc8: int  # ex> 0 매수호가 잔량 증감8
    bidp_rsqn_icdc9: int  # ex> 0 매수호가 잔량 증감9
    bidp_rsqn_icdc10: int  # ex> 0 매수호가 잔량 증감10
    total_askp_rsqn: int  # ex> 1119734 총 매도호가 잔량
    total_bidp_rsqn: int  # ex> 741434 총 매수호가 잔량
    total_askp_rsqn_icdc: int  # ex> 0 총 매도호가 잔량 증감
    total_bidp_rsqn_icdc: int  # ex> 0 총 매수호가 잔량 증감
    ovtm_total_askp_icdc: int  # ex> 0 시간외 총 매도호가 증감
    ovtm_total_bidp_icdc: int  # ex> 0 시간외 총 매수호가 증감
    ovtm_total_askp_rsqn: int  # ex> 3679 시간외 총 매도호가 잔량
    ovtm_total_bidp_rsqn: int  # ex> 0 시간외 총 매수호가 잔량
    ntby_aspr_rsqn: int  # ex> -378300 순매수 호가 잔량
    ''' ntby_aspr_rsqn
        '00' : 장전 예상체결가와 장마감 동시호가
        '49' : 장후 예상체결가
        (1) 첫 번째 비트
            1 : 장개시전
            2 : 장중
            3 : 장종료후
            4 : 시간외단일가
            7 : 일반Buy-in
            8 : 당일Buy-in
        (2) 두 번째 비트
            0 : 보통
            1 : 종가
            2 : 대량
            3 : 바스켓
            7 : 정리매매
            8 : Buy-in
    '''
    new_mkop_cls_code: str  # ex> 31 신 장운영 구분 코드


@dataclass_json
@dataclass
class NowPrice:
    ''' antc_mkop_cls_code
	    311 : 예상체결시작
        112 : 예상체결종료
    '''
    antc_mkop_cls_code: str  # 신 장운영 구분 코드 : 112
    stck_prpr: int  # 주식 현재가 ex) 171
    stck_oprc: int  # 주식 시가 ex) 172
    stck_hgpr: int  # 주식 최고가 ex) 173
    stck_lwpr: int  # 주식 최저가 ex) 167
    stck_sdpr: int  # 주식 기준가 ex) 173
    antc_cnpr: int  # 예상 체결가 ex) 171
    ''' antc_cntg_vrss_sign
    	1 : 상한
        2 : 상승
        3 : 보합
        4 : 하한
        5 : 하락
    '''
    antc_cntg_vrss_sign: str  # 예상 체결 대비 부호 ex) 5
    antc_cntg_vrss: int  # 예상 체결 대비 ex) -2
    antc_cntg_prdy_ctrt: float  # 예상 체결 전일 대비율 ex) -1.16
    antc_vol: int  # 예상 거래량 ex) 15795
    stck_shrn_iscd: str  # 주식 단축 종목코드 ex) 900110
    vi_cls_code: str  # VI 적용구분코드 ex) N


@dataclass_json
@dataclass
class AskingPriceExpCcn:
    code: str
    actual_time: datetime = field(  # 호가 접수 시간
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    data_received_time: datetime = field(  # 데이터 수집 시간
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        ))
    now_price: NowPrice
    ask_bid: AskBidPrice

    def make_redis_key(self):
        bz_yyyymmdd = self.actual_time.strftime("%Y%m%d")
        return AskingPriceExpCcn.static_make_redis_key(self.code, self.actual_time, bz_yyyymmdd)

    @staticmethod
    def static_make_redis_key(code: str, now_time: datetime, bz_yyyymmdd: str):
        return "%s.%s.%s" % (bz_yyyymmdd, now_time.strftime("%H%M"), code)

@dataclass_json
@dataclass
class AskingPriceExpCcnAll(BaseModelAll):
    items: List[AskingPriceExpCcn]

    def __init__(self) -> None:
        super().__init__()

    def add(self, data: AskingPriceExpCcn) -> None:
        super(AskingPriceExpCcnAll, self).add(data)
        return
