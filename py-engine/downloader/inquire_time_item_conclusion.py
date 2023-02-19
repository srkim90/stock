import datetime
import json
import os
import sys
import threading
import time
from typing import List

import requests
#sys.path.append("C://work//PyStock")
from common.access_token_provider import access_token_init
from common.holiday_provider import get_holiday_all
from common.stock_lock import StockLock
from models.holiday_models import HolidayAll
from models.time_item_conclusion_models import build_time_item_conclusion_all, TimeItemConclusionAll


from common.define import TIME_ITEM_CONCLUSION, MAX_DOWNLOAD_TH
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_base import InquireBase
from models.stock_code_models import StockCodeAll



# 주식현재가 당일시간대별체결[v1_국내주식-023]
class InquireTimeItemConclusion(InquireBase):
    holiday_all: HolidayAll
    lock: StockLock

    def __init__(self) -> None:
        self.lock = StockLock(MAX_DOWNLOAD_TH)
        sub_url = "/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion"
        tr_id = "FHPST01060000"
        sub_type = TIME_ITEM_CONCLUSION
        self.holiday_all = get_holiday_all()
        super().__init__(tr_id, sub_url, sub_type=sub_type)

    def __save_data(self, code: str, conclusion_all: TimeItemConclusionAll):
        name = "%s.json" % (code,)
        data = TimeItemConclusionAll.to_json(conclusion_all, indent=4, ensure_ascii=False)
        self._in_save_data(name, data, self.sub_type, sub_dir=self.holiday_all.get_last_bz_day_str())
        return

    def __request_at(self, idx: int, code: str):
        try:
            self.__request_at_2(idx, code)
        except Exception as e:
            sa_log("InquireTimeItemConclusion::__request_at : Exception : %s" % (e,))
        self.lock.decrease()

    def __request_at_2(self, idx: int, code: str):  # period => D, W, M
        # self.lock.increase()
        # codes: StockCodeAll = get_stock_codes()
        # item = codes.code_dict[code]
        # time.sleep(1.25)
        # sa_log("[%d/%d] class=InquireTimeItemConclusion, code=%s (%s) end" % (
        #     idx, len(codes.codes), code, item.item_make_ko))
        # self.lock.decrease()
        # return
        codes: StockCodeAll = get_stock_codes()
        item = codes.code_dict[code]
        session: requests.Session = requests.session()
        mast_conclusions: TimeItemConclusionAll = TimeItemConclusionAll()
        next_time = "160000"
        for jdx in range(10000):
            if next_time is None:
                break
            query_params = {
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": "%s" % code,
                "FID_INPUT_HOUR_1": next_time
            }
            api_result = self._base_json_request(query=query_params, session=session)
            if api_result is None:
                continue
            api_result_output2: List[dict] = api_result.output2

            conclusions = build_time_item_conclusion_all(code, api_result_output2)
            if len(api_result_output2) > 10:
                next_time = conclusions.get_last()
                mast_conclusions.add(conclusions.items)
            else:
                mast_conclusions.add(conclusions.items)
                break
            continue
            # self.__save_data(code, day_price_all)
        self.__save_data(code, mast_conclusions)
        sa_log("[%d/%d] class=InquireTimeItemConclusion, code=%s (%s) end" % (
            idx, len(codes.codes), code, item.item_make_ko))
        session.close()
        return

    def request(self):  # period => D, W, M
        codes: StockCodeAll = get_stock_codes()
        for idx, code in enumerate(codes.codes):
            self.lock.wait()
            self.lock.increase()
            h_thread = threading.Thread(target=self.__request_at, args=(idx, code))
            h_thread.daemon = True
            h_thread.start()
        self.lock.wait()


def main():
    access_token_init()
    e = InquireTimeItemConclusion()
    e.request()


if __name__ == "__main__":
    main()
