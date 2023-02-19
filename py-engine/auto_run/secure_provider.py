import base64
import gzip
import os
from typing import List

from common.define import KEY_STORE_PATH


def get_cybos_secure() -> List[str]:
    secure_path = os.path.join(KEY_STORE_PATH, "cybos_ipaddrs.dat.gz")
    with gzip.open(secure_path, "rb") as fd:
        secure = base64.b64decode(fd.read())
    for idx in range(4):
        secure = base64.b64decode(secure)
    secure = secure.decode("utf-8")
    return secure.split("|")


# def main():
#     a, b, c = get_cybos_secure()
#     print("a=%s, b=%s, c=%s" % (a, b, c))
#
#
# if __name__ == "__main__":
#     main()
