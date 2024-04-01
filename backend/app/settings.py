import os
from flask import Flask
from dotenv import load_dotenv


class Config:
    ENV_MODE: str
    DETA_KEY: str
    CACHE_TABLE: str

    def init_app(self, app: Flask) -> None:
        load_dotenv()

        for key, value in os.environ.items():
            app.config[key] = value
            setattr(self, key, value)


settings = Config()
