import base64
import datetime
import json
import math
import os
import shutil
import zipfile
from typing import Union, Tuple, List
import urllib.request

import pandas as pd

from common.define import KIS_CODE_DATA_PATH, KOSDAQ, KOSPI
from common.stock_code_spec import *
from common.utils import make_dirs, get_now_yyyymmdd
from models.stock_code_models import StockCode, StockCodeAll, stock_codes_merge


class kisCodeProvider:
    mst_path: str

    def __init__(self) -> None:
        super().__init__()
        self.mst_path = os.path.join(KIS_CODE_DATA_PATH, "mst")
        self.market_code_url = "https://new.real.download.dws.co.kr/common/master/%s_code.mst.zip"
        make_dirs([self.mst_path, ])

    def download_mst_all(self):
        self.__download_mst_file(KOSDAQ)
        self.__download_mst_file(KOSPI)

    def load_mst_file_all(self):
        kosdaq: StockCodeAll = self.__load_mst_file(KOSDAQ, kosdaq_field_specs, kosdaq_columns)
        kospi: StockCodeAll = self.__load_mst_file(KOSPI, kospi_field_specs, kospi_columns)
        return stock_codes_merge(kosdaq, kospi)

    def __download_mst_file(self, market: str) -> str:
        url = self.market_code_url % (market,)
        code_file = os.path.join(self.mst_path, "%s_%s_code.mst" % (market, get_now_yyyymmdd()))
        code_file_2 = os.path.join(self.mst_path, "%s_code.mst" % (market,))
        if os.path.exists(code_file) is True:
            return code_file
        zip_file = code_file + ".zip"
        urllib.request.urlretrieve(url, zip_file)
        os.chdir(self.mst_path)
        if os.path.exists(code_file_2):
            os.remove(code_file_2)
        mst_zip = zipfile.ZipFile(zip_file)
        mst_zip.extractall()
        mst_zip.close()
        if os.path.exists(zip_file):
            os.remove(zip_file)
        shutil.move(code_file_2, code_file)
        return code_file

    def __load_mst_file(self, market: str, field_specs: List[int], field_columns: List[str]) -> StockCodeAll:
        now_ms = datetime.datetime.now().microsecond

        file_name = os.path.join(self.mst_path, "%s_%s_code.mst" % (market, get_now_yyyymmdd()))
        tmp_fil1 = os.path.join(self.mst_path, "%s_code_%s_%s_part1.tmp" % (market, now_ms, os.getpid()))
        tmp_fil2 = os.path.join(self.mst_path, "%s_code_%s_%s_part2.tmp" % (market, now_ms, os.getpid()))

        wf1 = open(tmp_fil1, mode="w")
        wf2 = open(tmp_fil2, mode="w")

        with open(file_name, mode="r", encoding="cp949") as f:
            for row in f:
                if "kosdaq" == market:
                    rf1 = row[0:len(row) - 222]
                    rf1_1 = rf1[0:9].rstrip()
                    rf1_2 = rf1[9:21].rstrip()
                    rf1_3 = rf1[21:].strip()
                    wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                    rf2 = row[-222:]
                    wf2.write(rf2)
                else:
                    rf1 = row[0:len(row) - 228]
                    rf1_1 = rf1[0:9].rstrip()
                    rf1_2 = rf1[9:21].rstrip()
                    rf1_3 = rf1[21:].strip()
                    wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                    rf2 = row[-228:]
                    wf2.write(rf2)
        wf1.close()
        wf2.close()
        part1_columns = ['단축코드', '표준코드', '한글종목명']
        df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='cp949')

        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=field_columns)

        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        # clean temporary file and dataframe
        del (df1)
        del (df2)
        os.remove(tmp_fil1)
        os.remove(tmp_fil2)

        all_codes = self.__convert_dict_to_object(market, field_columns, df.to_dict())

        # json_save_path = os.path.join(self.mst_path, "%s_code.json" % (market,))
        # with open(json_save_path, "wb") as fd:
        #     fd.write(StockCodeAll.to_json(all_codes, indent=4, ensure_ascii=False).encode("utf-8"))
        return all_codes

    def __get_item_by_idx(self, idx: int, name: str, dict_data: dict):
        value = dict_data[name][idx]
        if type(value) == str:
            value_lower = value.lower()
            if value_lower == "n":
                value = False
            if value_lower == "y":
                value = True
            if value_lower == "nan":
                value = None
        if type(value) == float:
            if math.isnan(value) is True:
                value = None
        return value

    def __convert_dict_to_object(self, market: str, field_columns: List[str], dict_data: dict) -> StockCodeAll:
        codes: List[StockCode] = []
        n_item = len(dict_data['단축코드'].keys())
        for idx in range(n_item):
            details = {}
            for column in field_columns:
                details[column] = self.__get_item_by_idx(idx, column, dict_data)
            item = StockCode(
                market=market,
                shortcode=self.__get_item_by_idx(idx, "단축코드", dict_data),
                standard_code=self.__get_item_by_idx(idx, "표준코드", dict_data),
                item_make_ko=self.__get_item_by_idx(idx, "한글종목명", dict_data),
                details=details
            )
            codes.append(item)

        return StockCodeAll(items=codes, codes=[], code_dict={})


g_codes: StockCodeAll = None


def get_stock_codes() -> StockCodeAll:
    if g_codes is None:
        stock_code_init()
    return g_codes


def stock_code_init() -> StockCodeAll:
    global g_codes
    e = kisCodeProvider()
    e.download_mst_all()
    g_codes = e.load_mst_file_all()
    return g_codes


if __name__ == "__main__":
    get_stock_codes()
