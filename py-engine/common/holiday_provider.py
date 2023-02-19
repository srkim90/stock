import datetime
import json
import os

from common.define import DAY_PRICE, HOLIDAY
from common.stock_codes import get_stock_codes
from downloader.inquire_base import InquireBase
from models.daily_price_models import build_daily_price, DailyPrice, DailyPriceAll
from models.holiday_models import build_holiday, HolidayAll, Holiday, merge_holiday
from models.stock_code_models import StockCodeAll


class HolidayProvider(InquireBase):
    def __init__(self) -> None:
        sub_url = "/uapi/domestic-stock/v1/quotations/chk-holiday"
        tr_id = "CTCA0903R"
        sub_type = HOLIDAY
        super().__init__(tr_id, sub_url, sub_type=sub_type)

    def __save_data(self, holiday_all: HolidayAll):
        yyyymm_group = {}

        for item in holiday_all.items:
            yyyy = item.bass_dt.strftime("%Y")
            d_day_dict = Holiday.to_dict(item)
            try:
                yyyymm_group[yyyy].append(d_day_dict)
            except KeyError:
                yyyymm_group[yyyy] = [d_day_dict, ]
        for yyyy in yyyymm_group.keys():
            name = "%s.json" % (yyyy,)
            data = json.dumps(yyyymm_group[yyyy], indent=4, ensure_ascii=False)
            sub_type = HOLIDAY
            sub_dir = None
            self._in_save_data(name, data, sub_type, sub_dir)
        return

    def load_data(self) -> HolidayAll:
        return self.__load_data()

    def __load_data(self) -> HolidayAll:
        save_dir = self._get_data_save_dir()
        mast_holiday = HolidayAll()
        check_yyyy = [
            (datetime.date.today() - datetime.timedelta(4 * 365)).strftime("%Y"),  # 2019
            (datetime.date.today() - datetime.timedelta(3 * 365)).strftime("%Y"),  # 2020
            (datetime.date.today() - datetime.timedelta(2 * 365)).strftime("%Y"),  # 2021
            (datetime.date.today() - datetime.timedelta(1 * 365)).strftime("%Y"),  # 2022
            (datetime.date.today() + datetime.timedelta(0 * 365)).strftime("%Y"),  # 2023
            (datetime.date.today() + datetime.timedelta(1 * 365)).strftime("%Y")  # 2024
        ]
        for save_file_path in os.listdir(save_dir):
            yyyy = save_file_path.split(".")[0]
            if yyyy not in check_yyyy:
                continue
            save_file_path = os.path.join(save_dir, save_file_path)
            merge_holiday(mast_holiday, HolidayAll(items=self._in_load_data(save_file_path, Holiday, is_list=True)))
        #merge_holiday(mast_holiday, self.__request())
        return mast_holiday

    def __request(self) -> HolidayAll:  # period => D, W, M
        n_jump = 0
        holiday_all: HolidayAll = HolidayAll()
        start_day = datetime.date.today() - datetime.timedelta(44)
        for item in range(3):
            query_params = {
                "BASS_DT": (start_day - datetime.timedelta(n_jump)).strftime("%Y%m%d"),
                "CTX_AREA_NK": "",
                "CTX_AREA_FK": "",
            }
            api_result = self._base_json_request(query=query_params, add_header={"custtype": "P"})
            if api_result is None:
                break
            for a_day_result in api_result.output:
                now_holiday = build_holiday(a_day_result)
                if now_holiday.bass_dt.strftime("%Y%m%d") in holiday_all.yymmdd_dict.keys():
                    continue
                holiday_all.items.append(now_holiday)
                n_jump = (start_day - now_holiday.bass_dt.date()).days
            holiday_all.refresh()
        # self.__save_data(holiday_all)
        return holiday_all


g_holiday_all: HolidayAll = None


def holiday_init():
    global g_holiday_all
    provider: HolidayProvider = HolidayProvider()
    g_holiday_all = provider.load_data()


def get_holiday_all() -> HolidayAll:
    if g_holiday_all is None:
        holiday_init()
    return g_holiday_all

# def main():
#     e = HolidayProvider()
#     e.load_data()
#
#
# if __name__ == "__main__":
#     main()
