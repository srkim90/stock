import redis


class RedisDB:
    def __init__(self, ipaddr: str, port: int, passwd: str) -> None:
        super().__init__()
        self.ipaddr: str = ipaddr
        self.port: int = port
        self.passwd: str = passwd
        self.h_redis = self.__connect()

    def __connect(self):
        return redis.Redis(
                   host=self.ipaddr,
                   port=self.port,
                   password=self.passwd)

    def put(self, key: str, data: any, data_class: any = None) -> None:
        if type(data) is str:
            data = data.decode("utf-8")
        elif type(data) is bytes:
            pass
        else:
            data = data_class.to_json(data, indent=4, ensure_ascii=False).encode("utf-8")
        self.h_redis.set(key, data)

    def get(self, key: str, data_class: any = None) -> any:
        value = self.h_redis.get(key)
        if value is None or data_class is None:
            return value
        return data_class.from_json(value)