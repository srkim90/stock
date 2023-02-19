import datetime
from typing import List, Union

import win32com
from win32com.client import Dispatch

from common.tps_service import inc_cybos_tps
from common.utils import sa_log


class Win32Dispatch:
    win32_object: Dispatch

    def __init__(self, module_name: str) -> None:
        super().__init__()
        self.win32_object = win32com.client.Dispatch(module_name)

    def set_input_value(self, a, b) -> None:
        self.win32_object.SetInputValue(a, b)

    def send_block_request(self) -> bool:
        inc_cybos_tps()
        try:
            self.win32_object.BlockRequest()
        except Exception as e:
            sa_log("Error in win32_object.BlockRequest : error=%s" % (e,))
            return False
        return True

    def get_header_value(self, header_type: int) -> any:
        return self.win32_object.GetHeaderValue(header_type)

    def get_data_value(self, data_type: int, index: int) -> any:
        return self.win32_object.GetDataValue(data_type, index)

    def release(self):
        #elf.win32_object.
        pass

class InquireCybosBase:
    module_name: str
    today_yyyymmdd: str

    def __init__(self, module_name: str) -> None:
        super().__init__()
        self.today_yyyymmdd = datetime.datetime.now().strftime("%Y%m%d")
        self.module_name = module_name

    def _get_dispatch_object(self):
        return Win32Dispatch(self.module_name)

    def _check_code(self, codes: Union[str, List[str]]) -> Union[str, None]:
        if type(codes) == str:
            if len(codes) == 6:
                return "A" + codes
            else:
                return None
        elif type(codes) == list:
            if len(codes) == 0:
                return None
            new_codes = ""
            for item in codes:
                if len(item) == 6:
                    item = "A" + item
                else:
                    continue
                new_codes += "%s," % item
            if len(new_codes) == 0:
                return None
            return new_codes[0:-1]
        raise None
