from typing import Union


class BaseModelAll:
    def __init__(self) -> None:
        super().__init__()
        self.items = []

    def add(self, data: any) -> None:
        if len(self.items) > 0:
            if data.actual_time == self.items[-1].actual_time:
                return
        self.items.append(data)
        return

    def get_last(self) -> any:
        if len(self.items) == 0:
            return None
        return self.items[-1]
