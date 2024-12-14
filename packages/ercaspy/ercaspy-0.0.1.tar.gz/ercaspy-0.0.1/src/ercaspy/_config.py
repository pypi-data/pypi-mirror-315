class Config:
    __instance = None
    __secret_key: str | None = None
    __SANDBOX_URL = "https://api.merchant.staging.ercaspay.com/api/v1"
    __LIVE_URL = "https://api.ercas.com"

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of Config exists."""
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def API_URL(self):
        return (
            self.__LIVE_URL
            if (self.__secret_key and "LIVE" in self.__secret_key)
            else self.__SANDBOX_URL
        )

    @property
    def secret_key(self):
        return self.__secret_key

    @secret_key.setter
    def secret_key(self, value):
        self.__secret_key = value


config = Config()
