import os
from flask import Flask
from dotenv import load_dotenv


class Config:
    ENV_MODE: str
    DETA_PROJECT_KEY: str
    CACHE_TABLE: str
    FLASK_SECRET_KEY: str

    def init_app(self, app: Flask) -> None:
        load_dotenv()

        for key, value in os.environ.items():
            if key.startswith("FLASK_"):
                flask_key = key[6:]
                app.config[flask_key] = value

            setattr(self, key, value)


settings = Config()
