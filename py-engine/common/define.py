import os
import platform

#### 연동정보 ####
REDIS_SERVER_IP = "192.168.20.100"
REDIS_PASSWORD = "9998"
REDIS_PORT_MST2 = 7000
REDIS_ASKING_PRICE_EXP = 7001
REDIS_WORKER_TH = 4

#### SUB-TYPE ####
DAY_PRICE = "day-price"
HOLIDAY = "holiday"
DAY_ITEM_CHART_PRICE = "day-item-chart-price"
TIME_ITEM_CHART_PRICE = "time-item-chart-price"
TIME_ITEM_CONCLUSION = "time-item-conclusion"
STOCK_MST = "stock-mst"
ASKING_PRICE_EXP = "asking-price-exp-ccn"
TOP_N_CODE = "top-n-code"

#### PATH ####
from common.utils import make_dirs

if platform.system().lower() == "linux":
    BASE_DATA_DIR: str = "/srkim/new-stock"
else:
    BASE_DATA_DIR: str = "E:\\stock"
    if os.path.exists(BASE_DATA_DIR) is False:
        BASE_DATA_DIR = "Y:\\"

KEY_STORE_PATH: str = os.path.join(BASE_DATA_DIR, "secure")
DATA_PATH: str = os.path.join(BASE_DATA_DIR, "data")
KIS_CODE_DATA_PATH: str = os.path.join(DATA_PATH, "kis-code")
DAY_PRICE_DATA_PATH: str = os.path.join(DATA_PATH, DAY_PRICE)

make_dirs([BASE_DATA_DIR, KEY_STORE_PATH, KIS_CODE_DATA_PATH, DAY_PRICE_DATA_PATH])

#### URL ####
# OPEN_API_BASE_URL="https://openapivts.koreainvestment.com:29443" # 모의 투자
OPEN_API_BASE_URL = "https://openapi.koreainvestment.com:9443"  # 실전

#### 상수들 ####
KOSDAQ = "kosdaq"
KOSPI = "kospi"

MAX_DOWNLOAD_TH: int = 6
