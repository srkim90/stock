import datetime
import json
import os
import sys

from common.access_token_provider import access_token_init

sys.path.append("C://work//PyStock")
from common.define import DAY_ITEM_CHART_PRICE
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_base import InquireBase
from models.daily_itemchartprice_models import DailyItemChartPrice, build_daily_item_chart_price, DailyItemChartPriceAll
from models.daily_price_models import build_daily_price, DailyPrice, DailyPriceAll
from models.stock_code_models import StockCodeAll


# 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
class InquireDailyItemchartprice(InquireBase):
    def __init__(self) -> None:
        sub_url = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        tr_id = "FHKST03010100"
        self.max_chek_day = 365 * 10
        super().__init__(tr_id, sub_url)


    def __save_data(self, code: str, day_price_all: DailyItemChartPriceAll):
        yyyymm_group = {}
        for item in day_price_all.items:
            yyyymm = item.stck_bsop_date.strftime("%Y%m")
            d_day_dict = DailyPrice.to_dict(item)
            try:
                yyyymm_group[yyyymm].append(d_day_dict)
            except KeyError:
                yyyymm_group[yyyymm] = [d_day_dict,]
        for yyyymm in yyyymm_group.keys():
            name = "%s.json" % (code,)
            data = json.dumps(yyyymm_group[yyyymm], indent=4, ensure_ascii=False)
            sub_type = DAY_ITEM_CHART_PRICE
            sub_dir = yyyymm
            self._in_save_data(name, data, sub_type, sub_dir)
        return

    def request(self, period: str):  # period => D, W, M
        codes: StockCodeAll = get_stock_codes()
        for idx, code in enumerate(codes.codes):
            item = codes.code_dict[code]
            day_price_all: DailyItemChartPriceAll = DailyItemChartPriceAll()
            jdx = 0
            jump_unit = 125
            n_day_ago = 0
            while n_day_ago < self.max_chek_day:
                e_yyyymmdd = (datetime.date.today() - datetime.timedelta(n_day_ago)).strftime("%Y%m%d")
                s_yyyymmdd = (datetime.date.today() - datetime.timedelta(n_day_ago + jump_unit)).strftime("%Y%m%d")
                n_day_ago += jump_unit
                if jdx == 1: # 2번째 쿼리부터, 파일 존재시 다운 받지 않음
                    name = "%s.json" % (code,)
                    e_yyyymm = (datetime.date.today() - datetime.timedelta(n_day_ago)).strftime("%Y%m")
                    if os.path.exists(self.get_item_save_path(name, DAY_ITEM_CHART_PRICE, e_yyyymm)) is True:
                        sa_log("[daily-item-chart-price] skip download : code=%s" % (code,))
                        break
                query_params = {
                    "FID_COND_MRKT_DIV_CODE": "J",
                    "FID_INPUT_ISCD": code,
                    "FID_PERIOD_DIV_CODE": period,
                    "FID_ORG_ADJ_PRC": "0",
                    "FID_INPUT_DATE_1": s_yyyymmdd,
                    "FID_INPUT_DATE_2": e_yyyymmdd
                }
                api_result = self._base_json_request(query=query_params)
                if api_result is None:
                    continue
                for day_data_at in api_result.output2:
                    if len(day_data_at.keys()) == 0:
                        n_day_ago = 365 * 1024
                        break
                    day_price: DailyItemChartPrice = build_daily_item_chart_price(code, period, day_data_at)
                    day_price_all.items.append(day_price)
                jdx += 1
            self.__save_data(code, day_price_all)
            sa_log("[%d/%d] code: %s (%s) end" % (idx, len(codes.codes), code, item.item_make_ko))

def main():
    access_token_init()
    e = InquireDailyItemchartprice()
    e.request("D")



if __name__ == "__main__":
    main()
