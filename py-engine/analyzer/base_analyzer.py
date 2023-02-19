import datetime
from typing import List, Dict

from common.define import REDIS_SERVER_IP, REDIS_PORT_MST2, REDIS_PASSWORD, REDIS_ASKING_PRICE_EXP
from downloader.inquire_daily_price import InquireDailyPrice
from models.asking_price_exp_ccn_models import AskingPriceExpCcn
from models.daily_price_models import load_day_price_all, DailyPriceAll
from models.realtime_stock_session import RealtimeSession
from models.stock_mst2_models import StockMst2Models
from redis_db.redis_db import RedisDB
from service.select_top_n_code import SelectTopNCode


class BaseAnalyzer:
    codes: List[str]
    target_yyyymmdd: str
    session: RealtimeSession
    day_price_dict: Dict[str, DailyPriceAll]

    def __init__(self, target_yyyymmdd=None) -> None:
        super().__init__()
        self.day_price_dict = {}
        self.session = RealtimeSession()
        self.target_yyyymmdd = target_yyyymmdd
        self.day_price = InquireDailyPrice()
        self.codes = SelectTopNCode.get_code_n(500)
        self.redis_mst_db = RedisDB(REDIS_SERVER_IP, REDIS_PORT_MST2, REDIS_PASSWORD)
        self.redis_ask_db = RedisDB(REDIS_SERVER_IP, REDIS_ASKING_PRICE_EXP, REDIS_PASSWORD)

    def __get_day_price(self, code):
        try:
            return self.day_price_dict[code]
        except KeyError:
            self.day_price_dict[code] = self.day_price.load_data(code, 20)
        return self.day_price_dict[code]

    def __check_at(self, code: str):
        mst: StockMst2Models = self.session.get_last(code, StockMst2Models)
        ask: AskingPriceExpCcn = self.session.get_last(code, AskingPriceExpCcn)
        day: DailyPriceAll = self.__get_day_price(code)
        if mst is None or ask is None:
            return
        return None

    def __analyzer_at(self, code: str, time_at: datetime.datetime):
        hhmmss = time_at.strftime("%H:%M:%S")
        redis_mst_key = StockMst2Models.static_make_redis_key(code, time_at, self.target_yyyymmdd)
        redis_ack_key = AskingPriceExpCcn.static_make_redis_key(code, time_at, self.target_yyyymmdd)
        data_mst: StockMst2Models = self.redis_mst_db.get(redis_mst_key, StockMst2Models)
        data_ask: AskingPriceExpCcn = self.redis_ask_db.get(redis_ack_key, AskingPriceExpCcn)
        self.session.add(code, [data_mst, data_ask])
        # if data_mst is not None and data_ask is not None:
        #    print("%s->%s" % (code, hhmmss))
        if data_mst is not None:
            self.__check_at(code)
        return

    def analyzer(self):
        for code in self.codes:
            if code != "065440":
                continue
            for idx in range(13, 15):  # range(9, 15):
                for jdx in range(0, 60):
                    for kdx in range(0, 60, 10):
                        time_at = datetime.datetime.strptime("%s %02d%02d%02d" % (self.target_yyyymmdd, idx, jdx, kdx),
                                                             "%Y%m%d %H%M%S")
                        self.__analyzer_at(code, time_at)


def main():
    e = BaseAnalyzer(target_yyyymmdd="20230217")
    e.analyzer()
    return


if __name__ == "__main__":
    main()
