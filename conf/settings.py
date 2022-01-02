from pydantic import BaseSettings


class Settings(BaseSettings):
    STABLE_COINS = ["USDT", "USDC", "BUSD", "DAI", "UST", "TUSD"]

    # KuCoin
    KUCOIN_API_KEY: str
    KUCOIN_API_SECRET: str
    KICOIN_API_PASSPHRASE: str

    class Config:
        env_file = ".env"
