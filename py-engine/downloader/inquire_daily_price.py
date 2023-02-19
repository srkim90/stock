import datetime
import json
import os
from typing import Union

from common.access_token_provider import access_token_init
from common.define import DAY_PRICE
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_base import InquireBase
from models.daily_price_models import build_daily_price, DailyPrice, DailyPriceAll, load_day_price_all
from models.stock_code_models import StockCodeAll


# 주식현재가 일자별[v1_국내주식-010]
class InquireDailyPrice(InquireBase):
    def __init__(self) -> None:
        sub_url = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
        tr_id = "FHKST01010400"
        super().__init__(tr_id, sub_url)


    def __make_json_name(self, code:str) -> str:
        return "%s.json" % (code,)

    def __load_data(self, code: str, n_day_load: Union[int, None]) -> DailyPriceAll:
        sub_type = DAY_PRICE
        name = self.__make_json_name(code)
        base_dir = self._make_file_dir_name(sub_type)
        data_all: DailyPriceAll = DailyPriceAll()
        e_yyyymmdd = None
        if n_day_load is not None:
            e_yyyymmdd = int((datetime.date.today() - datetime.timedelta(n_day_load)).strftime("%Y%m"))
        for sub_type in os.listdir(base_dir):
            now_check_dir = os.path.join(base_dir, sub_type)
            if os.listdir(now_check_dir) is False:
                continue
            if len(sub_type) != 6:
                continue
            f_name = self._make_file_dir_name(base_dir, sub_type, name)
            if os.path.exists(f_name) is False:
                f_name += ".gz"
            if os.path.exists(f_name) is False:
                continue
            if e_yyyymmdd is not None:
                if e_yyyymmdd > int(sub_type):
                    continue
            data_obj = load_day_price_all(f_name)
            data_all.items += data_obj.items
        data_all.items.reverse()
        data_all.refresh()
        return data_all

    def load_data(self, code: str, n_day_load: Union[int, None]) -> DailyPriceAll:
        return self.__load_data(code, n_day_load)

    def __save_data(self, code: str, day_price_all: DailyPriceAll):
        yyyymm_group = {}
        for item in day_price_all.items:
            yyyymm = item.stck_bsop_date.strftime("%Y%m")
            d_day_dict = DailyPrice.to_dict(item)
            try:
                yyyymm_group[yyyymm].append(d_day_dict)
            except KeyError:
                yyyymm_group[yyyymm] = [d_day_dict, ]
        for yyyymm in yyyymm_group.keys():
            name = self.__make_json_name(code)
            data = json.dumps(yyyymm_group[yyyymm], indent=4, ensure_ascii=False)
            sub_type = DAY_PRICE
            sub_dir = yyyymm
            self._in_save_data(name, data, sub_type, sub_dir)
        return

    def request(self, period: str):  # period => D, W, M
        codes: StockCodeAll = get_stock_codes()
        for idx, code in enumerate(codes.codes):
            item = codes.code_dict[code]
            day_price_all: DailyPriceAll = DailyPriceAll()
            query_params = {
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": code,
                "FID_PERIOD_DIV_CODE": period,
                "FID_ORG_ADJ_PRC": "0"
            }
            api_result = self._base_json_request(query=query_params)
            if api_result is None:
                continue
            for day_data_at in api_result.output:
                day_price: DailyPrice = build_daily_price(code, period, day_data_at)
                day_price_all.items.append(day_price)
            self.__save_data(code, day_price_all)
            sa_log(
                "[%d/%d] class=InquireDailyPrice, code=%s (%s) end" % (idx, len(codes.codes), code, item.item_make_ko))


def main():
    access_token_init()
    e = InquireDailyPrice()
    e.request("D")


if __name__ == "__main__":
    main()
