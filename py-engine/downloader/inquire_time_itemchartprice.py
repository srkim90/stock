import sys

import requests
sys.path.append("C://work//PyStock")
from common.access_token_provider import access_token_init
from models.time_itemchartprice_models import build_time_item_chart_price, TimeItemChartPriceAll


from common.define import TIME_ITEM_CHART_PRICE
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_base import InquireBase
from models.daily_itemchartprice_models import DailyItemChartPrice, build_daily_item_chart_price, DailyItemChartPriceAll
from models.daily_price_models import build_daily_price, DailyPrice, DailyPriceAll
from models.stock_code_models import StockCodeAll


# 주식당일분봉조회[v1_국내주식-022]
class InquireTimeItemChartPrice(InquireBase):
    def __init__(self) -> None:
        sub_url = "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
        tr_id = "FHKST03010200"
        super().__init__(tr_id, sub_url)


    def __save_data(self, code: str, yyyymmdd: str, time_price_all: TimeItemChartPriceAll):
        name = "%s.json" % (code,)
        sub_dir = yyyymmdd
        data = TimeItemChartPriceAll.to_json(time_price_all, indent=4, ensure_ascii=False)
        self._in_save_data(name, data, TIME_ITEM_CHART_PRICE, sub_dir)
        return

    def request(self):  # period => D, W, M
        codes: StockCodeAll = get_stock_codes()
        for idx, code in enumerate(codes.codes):
            item = codes.code_dict[code]
            session: requests.Session = requests.session()
            next_time = "160000"
            all_chart: TimeItemChartPriceAll = TimeItemChartPriceAll()
            for jdx in range(10000):
                if next_time is None:
                    break
                query_params = {
                    "FID_ETC_CLS_CODE": "",
                    "FID_COND_MRKT_DIV_CODE": "J",
                    "FID_INPUT_ISCD": code,
                    "FID_INPUT_HOUR_1": next_time,
                    "FID_PW_DATA_INCU_YN": "N"
                }
                api_result = self._base_json_request(query=query_params, session=session)
                if api_result is None:
                    break
                for line in api_result.output2:
                    all_chart.items.append(build_time_item_chart_price(code, line))
                    next_time = line["stck_cntg_hour"]
                if len(api_result.output2) == 0 or '090000' == next_time:
                    break
            if len(all_chart.items) > 0:
                all_chart.items.reverse()
                self.__save_data(code, all_chart.items[0].stck_bsop_date.strftime("%Y%m%d"), all_chart)
                sa_log("[%d/%d] InquireTimeItemChartPrice code: %s (%s) end" % (idx, len(codes.codes), code, item.item_make_ko))
            continue

def main():
    access_token_init()
    e = InquireTimeItemChartPrice()
    e.request()



if __name__ == "__main__":
    main()
