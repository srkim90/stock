from dataclasses import dataclass
from typing import List, Dict, Union

from dataclasses_json import dataclass_json
''' 코스피
'그룹코드' = {str} 'ST'
'시가총액규모' = {float} 2.0
'지수업종대분류' = {int} 0
'지수업종중분류' = {int} 21
'지수업종소분류' = {int} 0
'제조업' = {bool} False
'저유동성' = {bool} False
'지배구조지수종목' = {bool} True
'KOSPI200섹터업종' = {str} '2'
'KOSPI100' = {bool} False
'KOSPI50' = {bool} False
'KRX' = {bool} True
'ETP' = {NoneType} None
'ELW발행' = {bool} False
'KRX100' = {bool} False
'KRX자동차' = {bool} False
'KRX반도체' = {bool} False
'KRX바이오' = {bool} False
'KRX은행' = {bool} False
'SPAC' = {bool} False
'KRX에너지화학' = {bool} False
'KRX철강' = {bool} False
'단기과열' = {int} 0
'KRX미디어통신' = {bool} False
'KRX건설' = {bool} False
'Non1' = {NoneType} None
'KRX증권' = {bool} False
'KRX선박' = {bool} False
'KRX섹터_보험' = {bool} False
'KRX섹터_운송' = {bool} False
'SRI' = {bool} True
'기준가' = {int} 87700
'매매수량단위' = {int} 1
'시간외수량단위' = {int} 1
'거래정지' = {bool} False
'정리매매' = {bool} False
'관리종목' = {bool} False
'시장경고' = {int} 0
'경고예고' = {bool} False
'불성실공시' = {bool} False
'우회상장' = {bool} False
'락구분' = {int} 0
'액면변경' = {int} 0
'증자구분' = {int} 0
'증거금비율' = {int} 50
'신용가능' = {bool} True
'신용기간' = {int} 90
'전일거래량' = {int} 80817
'액면가' = {int} 5000
'상장일자' = {int} 19730629
'상장주수' = {int} 16523
'자본금' = {int} 99290605000
'결산월' = {float} 12.0
'공모가' = {NoneType} None
'우선주' = {int} 0
'공매도과열' = {NoneType} None
'이상급등' = {bool} False
'KRX300' = {bool} True
'KOSPI' = {bool} True
'매출액' = {int} 120915
'영업이익' = {int} 8951
'경상이익' = {int} 3804
'당기순이익' = {int} -363
'ROE' = {float} -8.01
'기준년월' = {float} 20220930.0
'시가총액' = {int} 14491
'그룹사코드' = {str} '391'
'회사신용한도초과' = {bool} False
'담보대출가능' = {bool} False
'대주가능' = {bool} True
'''

''' ## 코스닥
'증권그룹구분코드' = {str} 'FS'
'시가총액 규모 구분 코드 유가' = {NoneType} None
'지수업종 대분류 코드' = {int} 0
'지수 업종 중분류 코드' = {int} 0
'지수업종 소분류 코드' = {int} 0
'벤처기업 여부 (Y/N)' = {bool} False
'저유동성종목 여부' = {bool} False
'KRX 종목 여부' = {bool} False
'ETP 상품구분코드' = {NoneType} None
'KRX100 종목 여부 (Y/N)' = {NoneType} None
'KRX 자동차 여부' = {bool} False
'KRX 반도체 여부' = {bool} False
'KRX 바이오 여부' = {bool} False
'KRX 은행 여부' = {bool} False
'기업인수목적회사여부' = {bool} False
'KRX 에너지 화학 여부' = {bool} False
'KRX 철강 여부' = {bool} False
'단기과열종목구분코드' = {int} 0
'KRX 미디어 통신 여부' = {bool} False
'KRX 건설 여부' = {bool} False
'(코스닥)투자주의환기종목여부' = {bool} False
'KRX 증권 구분' = {bool} False
'KRX 선박 구분' = {bool} False
'KRX섹터지수 보험여부' = {bool} False
'KRX섹터지수 운송여부' = {bool} False
'KOSDAQ150지수여부 (Y,N)' = {NoneType} None
'주식 기준가' = {int} 400
'정규 시장 매매 수량 단위' = {int} 1
'시간외 시장 매매 수량 단위' = {int} 1
'거래정지 여부' = {bool} False
'정리매매 여부' = {bool} False
'관리 종목 여부' = {bool} False
'시장 경고 구분 코드' = {int} 0
'시장 경고위험 예고 여부' = {bool} False
'불성실 공시 여부' = {bool} False
'우회 상장 여부' = {bool} False
'락구분 코드' = {int} 0
'액면가 변경 구분 코드' = {int} 0
'증자 구분 코드' = {int} 0
'증거금 비율' = {int} 100
'신용주문 가능 여부' = {bool} False
'신용기간' = {int} 90
'전일 거래량' = {int} 4213663
'주식 액면가' = {int} 0
'주식 상장 일자' = {int} 20160818
'상장 주수(천)' = {int} 82824
'자본금' = {int} 421606718
'결산 월' = {int} 12
'공모 가격' = {NoneType} None
'우선주 구분 코드' = {int} 0
'공매도과열종목여부' = {NoneType} None
'이상급등종목여부' = {bool} False
'KRX300 종목 여부 (Y/N)' = {NoneType} None
'매출액' = {int} 1067
'영업이익' = {int} 62
'경상이익' = {int} 36
'단기순이익' = {int} 15
'ROE(자기자본이익률)' = {int} 1
'기준년월' = {float} 20220930.0
'전일기준 시가총액 (억)' = {int} 331
'그룹사 코드' = {NoneType} None
'회사신용한도초과여부' = {bool} False
'담보대출가능여부' = {bool} False
'대주가능여부' = {bool} False
'''

@dataclass_json
@dataclass
class StockCode:
    market: str  # 소속 거래소
    shortcode: str  # 단축코드
    standard_code: int  # 표준코드
    item_make_ko: str  # 한글종목명
    details: dict  # 세부 데이터


@dataclass_json
@dataclass
class StockCodeAll:
    items: List[StockCode]

    # refresh 수행 시 자동 생설
    codes: List[str]
    code_dict: Dict[str, StockCode]

    def refresh(self):
        self.codes = []
        self.code_dict = {}
        for item in self.items:
            self.codes.append(item.shortcode)
            self.code_dict[item.shortcode] = item

    def get_length(self) -> int:
        return len(self.items)

    def get(self) -> List[StockCode]:
        return self.item

    def get_codes(self) -> List[str]:
        return self.codes

    def get_codes_filtering_by_trade(self, check_unit: int, market: Union[None, str] = None) -> List[str]:
        codes: List[str] = []
        for item in self.items:
            if type(market) is str:
                if item.market.lower() != market.lower():
                    continue
            if item.market == "kospi":
                trade = item.details["전일거래량"]
            else:
                trade = item.details["전일 거래량"]
            if trade >= check_unit:
                codes.append(item.shortcode)
        return codes

def stock_codes_merge(target_a: StockCodeAll, target_b: StockCodeAll) -> StockCodeAll:
    codes: StockCodeAll = StockCodeAll(items=target_a.items + target_b.items, codes=[], code_dict={})
    codes.refresh()
    return codes
