import datetime
import json
import os
from typing import Dict, List, Union

from common.define import BASE_DATA_DIR, TOP_N_CODE, DATA_PATH
from common.stock_codes import get_stock_codes
from common.utils import sa_log
from downloader.inquire_daily_price import InquireDailyPrice
from models.daily_price_models import DailyPriceAll, DailyPrice
from models.stock_code_models import StockCodeAll, StockCode


class SelectTopNCode:
    day_price: InquireDailyPrice
    base_date: datetime.datetime
    rank_table: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        # self.n_select = 500
        self.rank_table = {}
        self.day_price = InquireDailyPrice()
        self.base_date = None

    def __calc_rank(self, day_all: DailyPriceAll) -> Union[int, None]:
        acml_vol = 0
        if self.base_date is None:
            self.base_date = day_all.items[0].stck_bsop_date

        for idx, item in enumerate(day_all.items):
            item: DailyPrice
            acml_vol += (item.acml_vol * item.stck_clpr)
            if idx > 10:
                break
            if item.stck_clpr < 1000:
                return None
        return acml_vol

    @staticmethod
    def get_code_all(yyyymmdd=None) -> List[str]:
        if yyyymmdd is None:
            full_path = os.path.join(DATA_PATH, TOP_N_CODE, "codes.json")
        else:
            full_path = os.path.join(DATA_PATH, TOP_N_CODE, "%s.json" % yyyymmdd)
        with open(full_path, "rb") as fd:
            return json.loads(fd.read())

    @staticmethod
    def get_code_n(n_list: int, yyyymmdd=None) -> List[str]:
        return SelectTopNCode.get_code_all(yyyymmdd)[0:n_list]

    @staticmethod
    def get_code_range(s_idx: int, e_idx: int, yyyymmdd=None) -> List[str]:
        return SelectTopNCode.get_code_all(yyyymmdd)[s_idx:e_idx]

    def request(self) -> List[StockCode]:
        result_list: List[StockCode] = []
        codes: StockCodeAll = get_stock_codes()
        for idx, code in enumerate(codes.codes):
            item = codes.code_dict[code]
            day_all: DailyPriceAll = self.day_price.load_data(code, 20)
            score = self.__calc_rank(day_all)
            if score is None:
                continue
            self.rank_table[code] = score
            sa_log("[%d/%d] code: %s (%s) end" % (idx, len(codes.codes), code, item.item_make_ko))
            # if idx == 300:
            #    break
        sorted_dict = sorted(self.rank_table.items(), key=lambda item: item[1], reverse=True)
        # if len(sorted_dict) > self.n_select:
        #    sorted_dict = sorted_dict[0:self.n_select]
        for pair in sorted_dict:
            result_list.append(codes.code_dict[pair[0]])
        return result_list

    def save(self, code_list: List[StockCode]):
        str_code_list: List[str] = []
        str_code_list_full: List[str] = []
        save_dir = os.path.join(DATA_PATH, TOP_N_CODE)
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        full_path = os.path.join(DATA_PATH, TOP_N_CODE, "%s.json" % self.base_date.strftime("%Y%m%d"))
        full_path_full = os.path.join(DATA_PATH, TOP_N_CODE, "%s_full.json" % self.base_date.strftime("%Y%m%d"))
        full_path_2 = os.path.join(DATA_PATH, TOP_N_CODE, "codes.json")
        full_path_full_2 = os.path.join(DATA_PATH, TOP_N_CODE, "codes_full.json")
        for code in code_list:
            str_code_list_full.append(StockCode.to_dict(code))
            str_code_list.append(code.shortcode)
        with open(full_path, "wb") as fd:
            fd.write(json.dumps(str_code_list, indent=4, ensure_ascii=False).encode("utf-8"))
        with open(full_path_full, "wb") as fd:
            fd.write(json.dumps(str_code_list_full, indent=4, ensure_ascii=False).encode("utf-8"))
        with open(full_path_2, "wb") as fd:
            fd.write(json.dumps(str_code_list, indent=4, ensure_ascii=False).encode("utf-8"))
        with open(full_path_full_2, "wb") as fd:
            fd.write(json.dumps(str_code_list_full, indent=4, ensure_ascii=False).encode("utf-8"))
        return


def main():
    e = SelectTopNCode()
    result = e.request()
    e.save(result)
    return


if __name__ == "__main__":
    main()
