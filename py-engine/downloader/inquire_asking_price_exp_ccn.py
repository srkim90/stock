import datetime
import json
import os
import sys
import threading
import time
from typing import List
sys.path.append("Z://")
from common.holiday_provider import get_holiday_all
from models.asking_price_exp_ccn_models import AskBidPrice, NowPrice, AskingPriceExpCcn
from redis_db.redis_worker import RedisWorker
from service.select_top_n_code import SelectTopNCode

sys.path.append("C://work//PyStock")
from common.define import DAY_ITEM_CHART_PRICE, ASKING_PRICE_EXP, REDIS_SERVER_IP, REDIS_PORT_MST2, REDIS_PASSWORD, \
    REDIS_ASKING_PRICE_EXP
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_base import InquireBase
from models.daily_itemchartprice_models import DailyItemChartPrice, build_daily_item_chart_price, DailyItemChartPriceAll
from models.daily_price_models import build_daily_price, DailyPrice, DailyPriceAll
from models.stock_code_models import StockCodeAll


# 주식현재가 호가 예상체결[v1_국내주식-011]
class InquireAskingPriceExpCcn(InquireBase):
    bz_day: datetime.datetime
    target_codes: List[str]
    codes: StockCodeAll
    last_call: datetime.datetime

    def __init__(self, s_idx: int, e_idx: int, tps: float) -> None:
        sub_url = "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
        tr_id = "FHKST01010200"
        self.tps = tps
        self.last_call = datetime.datetime.now()
        self.bz_day_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        self.target_codes = SelectTopNCode.get_code_range(s_idx, e_idx)
        self.codes = get_stock_codes()
        self.last_hhmm = {}
        self.redis_works = RedisWorker(REDIS_SERVER_IP, REDIS_ASKING_PRICE_EXP, REDIS_PASSWORD)
        super().__init__(tr_id, sub_url)

    def __update_db(self, asking_price: AskingPriceExpCcn):
        key = asking_price.make_redis_key()
        self.redis_works.put(key, asking_price, AskingPriceExpCcn)

    def __save_data(self, code: str, asking_price: AskingPriceExpCcn) -> None:
        name = "%s.json.gz" % (code,)
        sub_type = ASKING_PRICE_EXP
        hhmm = asking_price.actual_time.strftime("%H%M")
        try:
            last = self.last_hhmm[code]
            if last == hhmm:
                return
        except KeyError:
            self.last_hhmm[code] = hhmm
        sub_dir = [self.bz_day_yyyymmdd, "%s" % (hhmm,)]  # [0:-1] + "0",)]
        self.last_hhmm[code] = hhmm
        self._in_save_data(name, asking_price, sub_type, sub_dir, data_type=AskingPriceExpCcn, allow_overwrite=False)
        self.__update_db(asking_price)
        return

    def wait(self) -> None:
        ms = (datetime.datetime.now() - self.last_call).microseconds / 1000
        interval = (1000 / self.tps) - ms
        if interval < 0:
            return
        interval = interval / 1000.0
        # print(interval)
        time.sleep(interval)

    def request(self):  # period => D, W, M
        self.bz_day_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        for idx, code in enumerate(self.target_codes):  # enumerate(codes.codes):
            item = self.codes.code_dict[code]
            self.wait()
            query_params = {
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": "%s" % code,
            }
            api_result = self._base_json_request(query=query_params)
            if api_result is None:
                continue
            output = api_result.output1
            ask_bid = AskBidPrice(
                aspr_acpt_hour=datetime.datetime.strptime("%s_%s" % (self.bz_day_yyyymmdd, output["aspr_acpt_hour"]),
                                                          "%Y%m%d_%H%M%S"),
                askp1=int(output["askp1"]),  # ex>  171
                askp2=int(output["askp2"]),  # ex>  172
                askp3=int(output["askp3"]),  # ex>  173
                askp4=int(output["askp4"]),  # ex>  174
                askp5=int(output["askp5"]),  # ex>  175
                askp6=int(output["askp6"]),  # ex>  176
                askp7=int(output["askp7"]),  # ex>  177
                askp8=int(output["askp8"]),  # ex>  178
                askp9=int(output["askp9"]),  # ex>  179
                askp10=int(output["askp10"]),  # ex>  180
                bidp1=int(output["bidp1"]),  # ex>  170
                bidp2=int(output["bidp2"]),  # ex>  169
                bidp3=int(output["bidp3"]),  # ex>  168
                bidp4=int(output["bidp4"]),  # ex>  167
                bidp5=int(output["bidp5"]),  # ex>  166
                bidp6=int(output["bidp6"]),  # ex>  165
                bidp7=int(output["bidp7"]),  # ex>  164
                bidp8=int(output["bidp8"]),  # ex>  163
                bidp9=int(output["bidp9"]),  # ex>  162
                bidp10=int(output["bidp10"]),  # ex>  161
                askp_rsqn1=int(output["askp_rsqn1"]),  # ex>  37690
                askp_rsqn2=int(output["askp_rsqn2"]),  # ex>  225465
                askp_rsqn3=int(output["askp_rsqn3"]),  # ex>  90180
                askp_rsqn4=int(output["askp_rsqn4"]),  # ex>  83160
                askp_rsqn5=int(output["askp_rsqn5"]),  # ex>  102743
                askp_rsqn6=int(output["askp_rsqn6"]),  # ex>  111120
                askp_rsqn7=int(output["askp_rsqn7"]),  # ex>  113592
                askp_rsqn8=int(output["askp_rsqn8"]),  # ex>  70400
                askp_rsqn9=int(output["askp_rsqn9"]),  # ex>  178626
                askp_rsqn10=int(output["askp_rsqn10"]),  # ex>  106758
                bidp_rsqn1=int(output["bidp_rsqn1"]),  # ex>  3468
                bidp_rsqn2=int(output["bidp_rsqn2"]),  # ex>  306582
                bidp_rsqn3=int(output["bidp_rsqn3"]),  # ex>  106059
                bidp_rsqn4=int(output["bidp_rsqn4"]),  # ex>  137744
                bidp_rsqn5=int(output["bidp_rsqn5"]),  # ex>  50139
                bidp_rsqn6=int(output["bidp_rsqn6"]),  # ex>  33792
                bidp_rsqn7=int(output["bidp_rsqn7"]),  # ex>  36525
                bidp_rsqn8=int(output["bidp_rsqn8"]),  # ex>  44620
                bidp_rsqn9=int(output["bidp_rsqn9"]),  # ex>  3430
                bidp_rsqn10=int(output["bidp_rsqn10"]),  # ex>  19075
                askp_rsqn_icdc1=int(output["askp_rsqn_icdc1"]),  # ex>  0
                askp_rsqn_icdc2=int(output["askp_rsqn_icdc2"]),  # ex>  0
                askp_rsqn_icdc3=int(output["askp_rsqn_icdc3"]),  # ex>  0
                askp_rsqn_icdc4=int(output["askp_rsqn_icdc4"]),  # ex>  0
                askp_rsqn_icdc5=int(output["askp_rsqn_icdc5"]),  # ex>  0
                askp_rsqn_icdc6=int(output["askp_rsqn_icdc6"]),  # ex>  0
                askp_rsqn_icdc7=int(output["askp_rsqn_icdc7"]),  # ex>  0
                askp_rsqn_icdc8=int(output["askp_rsqn_icdc8"]),  # ex>  0
                askp_rsqn_icdc9=int(output["askp_rsqn_icdc9"]),  # ex>  0
                askp_rsqn_icdc10=int(output["askp_rsqn_icdc10"]),  # ex>  0
                bidp_rsqn_icdc1=int(output["bidp_rsqn_icdc1"]),  # ex>  0
                bidp_rsqn_icdc2=int(output["bidp_rsqn_icdc2"]),  # ex>  0
                bidp_rsqn_icdc3=int(output["bidp_rsqn_icdc3"]),  # ex>  0
                bidp_rsqn_icdc4=int(output["bidp_rsqn_icdc4"]),  # ex>  0
                bidp_rsqn_icdc5=int(output["bidp_rsqn_icdc5"]),  # ex>  0
                bidp_rsqn_icdc6=int(output["bidp_rsqn_icdc6"]),  # ex>  0
                bidp_rsqn_icdc7=int(output["bidp_rsqn_icdc7"]),  # ex>  0
                bidp_rsqn_icdc8=int(output["bidp_rsqn_icdc8"]),  # ex>  0
                bidp_rsqn_icdc9=int(output["bidp_rsqn_icdc9"]),  # ex>  0
                bidp_rsqn_icdc10=int(output["bidp_rsqn_icdc10"]),  # ex>  0
                total_askp_rsqn=int(output["total_askp_rsqn"]),  # ex>  1119734
                total_bidp_rsqn=int(output["total_bidp_rsqn"]),  # ex>  741434
                total_askp_rsqn_icdc=int(output["total_askp_rsqn_icdc"]),  # ex>  0
                total_bidp_rsqn_icdc=int(output["total_bidp_rsqn_icdc"]),  # ex>  0
                ovtm_total_askp_icdc=int(output["ovtm_total_askp_icdc"]),  # ex>  0
                ovtm_total_bidp_icdc=int(output["ovtm_total_bidp_icdc"]),  # ex>  0
                ovtm_total_askp_rsqn=int(output["ovtm_total_askp_rsqn"]),  # ex>  3679
                ovtm_total_bidp_rsqn=int(output["ovtm_total_bidp_rsqn"]),  # ex>  0
                ntby_aspr_rsqn=int(output["ntby_aspr_rsqn"]),  # ex>  -378300
                new_mkop_cls_code=output["new_mkop_cls_code"],  # ex>  "31"
            )
            output = api_result.output2
            now_price = NowPrice(
                antc_mkop_cls_code=output["antc_mkop_cls_code"],  # 신 장운영 구분 코드 = 112
                stck_prpr=int(output["stck_prpr"]),  # 주식 현재가 ex) 171
                stck_oprc=int(output["stck_oprc"]),  # 주식 시가 ex) 172
                stck_hgpr=int(output["stck_hgpr"]),  # 주식 최고가 ex) 173
                stck_lwpr=int(output["stck_lwpr"]),  # 주식 최저가 ex) 167
                stck_sdpr=int(output["stck_sdpr"]),  # 주식 기준가 ex) 173
                antc_cnpr=int(output["antc_cnpr"]),  # 예상 체결가 ex) 171
                antc_cntg_vrss_sign=output["antc_cntg_vrss_sign"],  # 예상 체결 대비 부호 ex) 5
                antc_cntg_vrss=int(output["antc_cntg_vrss"]),  # 예상 체결 대비 ex) -2
                antc_cntg_prdy_ctrt=float(output["antc_cntg_prdy_ctrt"]),  # 예상 체결 전일 대비율 ex) -1.16
                antc_vol=int(output["antc_vol"]),  # 예상 거래량 ex) 15795
                stck_shrn_iscd=output["stck_shrn_iscd"],  # 주식 단축 종목코드 ex) 900110
                vi_cls_code=output["vi_cls_code"]  # VI 적용구분코드 ex) N
            )

            asking_price: AskingPriceExpCcn = AskingPriceExpCcn(
                code=code,
                actual_time=ask_bid.aspr_acpt_hour,
                data_received_time=datetime.datetime.now(),
                now_price=now_price,
                ask_bid=ask_bid)
            self.__save_data(code, asking_price)
            sa_log("[%d/%d] code: %s (%s) end" % (idx, len(self.target_codes), code, item.item_make_ko))


def inquire_th_main(s_idx: int, e_idx: int, tps: float):
    e = InquireAskingPriceExpCcn(s_idx, e_idx, tps)
    while True:
        now_hh = datetime.datetime.now().hour
        if 8 <= now_hh <= 16:
            e.request()
        else:
            sa_log("sleeping.. : now_hh=%d" % now_hh)
            time.sleep(10.0)


def start_inquire_th(s_idx: int, e_idx: int, tps: float):
    h_thread = threading.Thread(target=inquire_th_main, args=(s_idx, e_idx, tps))
    h_thread.daemon = True
    h_thread.start()


def main():
    start_inquire_th(0, 1450, 4.85)
    time.sleep(5.0)
    start_inquire_th(1450, 2900, 4.85)

    while True:
        time.sleep(1.0)


if __name__ == "__main__":
    main()
