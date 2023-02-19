from typing import Dict

from common.utils import sa_log
from models.asking_price_exp_ccn_models import AskingPriceExpCcnAll, AskingPriceExpCcn
from models.base_model_all import BaseModelAll
from models.stock_mst2_models import StockMst2ModelsAll, StockMst2Models


class RealtimeSession:
    mst_dict: Dict[str, StockMst2ModelsAll]
    ask_dict: Dict[str, AskingPriceExpCcnAll]

    def __init__(self) -> None:
        super().__init__()
        self.mst_dict = {}
        self.ask_dict = {}

    def __get_dict_by_type(self, data: any) -> Dict[str, any]:
        if type(data) == StockMst2ModelsAll or type(data) == StockMst2Models or data == StockMst2ModelsAll or data == StockMst2Models:
            return self.mst_dict
        elif type(data) == AskingPriceExpCcnAll or type(data) == AskingPriceExpCcn or data == AskingPriceExpCcnAll or data == AskingPriceExpCcn:
            return self.ask_dict

    def get_last(self, code: str, data_type: any) -> any:
        try:
            data_all: BaseModelAll = self.__get_dict_by_type(data_type)[code]
        except KeyError as e:
            return None
        return data_all.get_last()

    def add(self, code: str, data: any):
        if type(data) == list or type(data) == tuple:
            pass
        else:
            data = [data,]
        for data_at in data:
            if type(data_at) == StockMst2Models:
                self.__add_mst(code, data_at)
            elif type(data_at) == AskingPriceExpCcn:
                self.__add_ask(code, data_at)
            elif data_at is None:
                continue
            else:
                sa_log("[RealtimeSession::add] Error. invalid of data type : %s" % (type(data)))
        return

    def __add_mst(self, code: str, data: StockMst2Models):
        try:
            chart: StockMst2ModelsAll = self.mst_dict[code]
        except KeyError:
            self.mst_dict[code] = StockMst2ModelsAll()
            chart: StockMst2ModelsAll = self.mst_dict[code]
        chart.add(data)
        return

    def __add_ask(self, code: str, data: AskingPriceExpCcn):
        try:
            chart: AskingPriceExpCcnAll = self.ask_dict[code]
        except KeyError:
            self.ask_dict[code] = AskingPriceExpCcnAll()
            chart: AskingPriceExpCcnAll = self.ask_dict[code]
        chart.add(data)
        return
