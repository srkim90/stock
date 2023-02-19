
echo "## 자동실행 : https://extrememanual.net/34339"
timeout 600
Z:
python Z:\cybos_downloader\inquery_connection_test.py
timeout 60
python Z:\cybos_downloader\inquire_cybos_stock_mst2.py
timeout 86400
