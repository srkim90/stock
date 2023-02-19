import datetime
import gzip
import os
import sys
import threading
import time
from multiprocessing import Process
from typing import List, Dict, Union

sys.path.append("Z://")
from common.define import DATA_PATH, STOCK_MST, REDIS_SERVER_IP, REDIS_PORT_MST2, REDIS_PASSWORD
from common.holiday_provider import holiday_init, get_holiday_all
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from redis_db.redis_worker import RedisWorker
from cybos_downloader.inquire_cybos_base import InquireCybosBase
from models.stock_mst2_models import StockMst2Models, StockMst2ModelsAll


class InquireCybosStockMst2(InquireCybosBase):
    market: Union[None, str]
    redis_works: RedisWorker
    last_check_time: Dict[str, datetime.datetime]

    def __init__(self, market: Union[None, str] = None) -> None:
        super().__init__("DsCbo1.StockMst2")
        self.redis_works = RedisWorker(REDIS_SERVER_IP, REDIS_PORT_MST2, REDIS_PASSWORD)
        self.market = market
        self.last_check_time = {}

    def __request_a_item(self, code_list: List[str]) -> List[StockMst2Models]:
        result_list = []
        new_code_list = self._check_code(code_list)  # 0 - (string) 다수의종목코드(구분자:',' , MAX: 110종목) 예) A003540,
        if new_code_list is None:
            return result_list
        com_object = self._get_dispatch_object()
        com_object.set_input_value("0", new_code_list)
        if com_object.send_block_request() is False:
            sa_log("Fail to send_block_request : code_list=%s" % (code_list,))
            return result_list
        count = com_object.get_header_value(0)  # 0 - (short) count
        bz_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        data_received_time = datetime.datetime.now()
        for idx in range(count):
            actual_time = datetime.datetime.strptime("%s_%s00" % (bz_yyyymmdd, com_object.get_data_value(2, idx)),
                                                     "%Y%m%d_%H%M%S")
            model = StockMst2Models(code=com_object.get_data_value(0, idx).replace("A", ""),
                                    name=com_object.get_data_value(1, idx),
                                    actual_time=actual_time,
                                    data_received_time=data_received_time,
                                    price=com_object.get_data_value(3, idx),
                                    전일대비=com_object.get_data_value(4, idx),
                                    상태구분=com_object.get_data_value(5, idx),
                                    시가=com_object.get_data_value(6, idx),
                                    고가=com_object.get_data_value(7, idx),
                                    저가=com_object.get_data_value(8, idx),
                                    매도호가=com_object.get_data_value(9, idx),
                                    매수호가=com_object.get_data_value(10, idx),
                                    거래량=com_object.get_data_value(11, idx),
                                    거래대금=com_object.get_data_value(12, idx),
                                    총매도잔량=com_object.get_data_value(13, idx),
                                    총매수잔량=com_object.get_data_value(14, idx),
                                    매도잔량=com_object.get_data_value(15, idx),
                                    매수잔량=com_object.get_data_value(16, idx),
                                    상장주식수=com_object.get_data_value(17, idx),
                                    외국인보유비율=com_object.get_data_value(18, idx),
                                    전일종가=com_object.get_data_value(19, idx),
                                    전일거래량=com_object.get_data_value(20, idx),
                                    체결강도=com_object.get_data_value(21, idx),
                                    순간체결량=com_object.get_data_value(22, idx),
                                    체결가비교=com_object.get_data_value(23, idx),
                                    호가비교=com_object.get_data_value(24, idx),
                                    동시호가구분=com_object.get_data_value(25, idx),
                                    예상체결가=com_object.get_data_value(26, idx),
                                    예상체결가_전일대비=com_object.get_data_value(27, idx),
                                    예상체결가_상태구분=com_object.get_data_value(28, idx),
                                    예상체결가_거래량=com_object.get_data_value(29, idx))
            result_list.append(model)
        return result_list

    def __start_update_file(self, stock: List[StockMst2Models]):
        h_thread = threading.Thread(target=self.__update_file, args=(stock,))
        h_thread.daemon = True
        h_thread.start()

    def __update_file(self, stock: List[StockMst2Models]) -> None:
        if len(stock) == 0:
            return
        s_time = datetime.datetime.now()
        bz_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        save_path = os.path.join(DATA_PATH, STOCK_MST, bz_yyyymmdd)
        if os.path.exists(save_path) is False:
            os.makedirs(save_path)
        market = "" if self.market is None else self.market + "_"
        file_name = os.path.join(save_path, "%s%s.json.gz" % (market, datetime.datetime.now().strftime("%H%M%S"),))
        with gzip.open(file_name, "wb") as fd:
            json_data: str = StockMst2ModelsAll.to_json(StockMst2ModelsAll(items=stock), indent=4, ensure_ascii=False)
            fd.write(json_data.encode("utf-8"))
        e_time = datetime.datetime.now()
        sa_log("InquireCybosStockMst2 : update time -> %s ms" % ((e_time - s_time).microseconds / 1000,))
        return

    def __update_db(self, stock: StockMst2Models, now_time: datetime.datetime, bz_yyyymmdd: str):
        key = stock.make_redis_key(now_time, bz_yyyymmdd)
        self.redis_works.put(key, stock, StockMst2Models)

    def __update(self, stock_mst: List[StockMst2Models], now_time: datetime.datetime) -> List[StockMst2Models]:
        new_list = []
        bz_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        for item in stock_mst:
            try:
                last = self.last_check_time[item.code]
                if item.actual_time == last:
                    continue
            except KeyError:
                self.last_check_time[item.code] = item.actual_time
            self.__update_db(item, now_time, bz_yyyymmdd)
            new_list.append(item)
        return new_list

    @staticmethod
    def wait() -> datetime.datetime:
        time.sleep(1)
        while True:
            time.sleep(0.1)
            now_time = datetime.datetime.now()
            if now_time.second % 10 == 0:
                return now_time

    @staticmethod
    def __check_time() -> bool:
        now_time = datetime.datetime.now()
        bz_yyyymmdd = get_holiday_all().get_last_bz_day().strftime("%Y%m%d")
        today_yyyymmdd = now_time.strftime("%Y%m%d")
        if bz_yyyymmdd == today_yyyymmdd and 8 <= now_time.hour <= 16:
            return True
        sa_log(" sleeping : bz_yyyymmdd=%s, today_yyyymmdd=%s, hour=%s" % (bz_yyyymmdd, today_yyyymmdd, now_time.hour))
        time.sleep(10.0)
        return False

    def test(self) -> bool:
        samsung_code = "005930"
        code_list = [samsung_code, ]
        result_list = self.__request_a_item(code_list)
        if len(result_list) == 0:
            sa_log("Fail to load stock data : length of result_list is 0")
            return False
        elif result_list[0].code != samsung_code:
            sa_log("Fail to load stock data : invalid samsung_code : %s, true code is :%s " % (result_list[0].code, samsung_code, ))
            return False
        return True

    def request(self, now_time: datetime.datetime) -> None:  # API 32번 call
        if self.__check_time() is False:
            return
        n_split_unit = 110
        stock_code_all = get_stock_codes().get_codes_filtering_by_trade(1000, market=self.market)
        stock_mst = []
        for idx in range(int(len(stock_code_all) / n_split_unit) + 2):
            s_idx = n_split_unit * idx
            e_idx = n_split_unit * (idx + 1)
            if s_idx >= len(stock_code_all):
                continue
            if e_idx > len(stock_code_all):
                e_idx = len(stock_code_all)
            code_list = stock_code_all[s_idx:e_idx]
            result_list = self.__request_a_item(code_list)
            result_list = self.__update(result_list, now_time)
            stock_mst += result_list
        self.__start_update_file(stock_mst)


def main():
    markets = ["kospi", "kosdaq"]
    proc_all = []
    for market in markets:
        proc = Process(target=run, args=(market,))
        proc.start()
        proc_all.append(proc)
        time.sleep(4.5)
    for proc in proc_all:
        proc.join()


def run(market: Union[None, str] = None):
    holiday_init()
    e = InquireCybosStockMst2(market=market)
    while True:
        now_time = e.wait()
        e.request(now_time)


if __name__ == "__main__":
    main()
