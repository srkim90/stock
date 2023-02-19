#!/bin/bash
BASE_DIR="/c/work"
BASE_DIR_COPY_TO="${BASE_DIR}/PyStock"
BASE_DIR_COPY_FROM="${BASE_DIR}/stock/py-engine"
NOW_TIME=`date "+%Y%m%d_%H%M%S"`
cp -r $BASE_DIR_COPY_TO ${BASE_DIR}/PyStock_bk/${NOW_TIME}

rm -rf ${BASE_DIR_COPY_TO}/common
rm -rf ${BASE_DIR_COPY_TO}/cybos_downloader
rm -rf ${BASE_DIR_COPY_TO}/*.py
rm -rf ${BASE_DIR_COPY_TO}/downloader
rm -rf ${BASE_DIR_COPY_TO}/models
rm -rf ${BASE_DIR_COPY_TO}/redis_db
rm -rf ${BASE_DIR_COPY_TO}/auto_run
rm -rf ${BASE_DIR_COPY_TO}/batch
rm -rf ${BASE_DIR_COPY_TO}/service

cp -r ${BASE_DIR_COPY_FROM}/common ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/cybos_downloader ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/*.py ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/downloader ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/models ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/redis_db ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/auto_run ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/batch ${BASE_DIR_COPY_TO}
cp -r ${BASE_DIR_COPY_FROM}/service ${BASE_DIR_COPY_TO}

# C:\work\PyStock-main\copy.sh