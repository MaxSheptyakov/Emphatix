import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool

@dataclass
class OpenAI:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    openai: OpenAI



def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_id=tg_bot.getint("admin_id"),
            use_redis=tg_bot.getboolean("use_redis"),
        ),
        db=DbConfig(**config["db"]),
        openai=OpenAI(token=config['openai'].get('openai_token')),
    )



config = load_config('bot.ini')
