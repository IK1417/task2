from dataclasses import dataclass
import configparser


@dataclass
class BotConfig:
    token: str
    admins_id: list[int]


def load_bot_config(path: str) -> BotConfig:
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    admins_list: list[int] = [
        int(admin_id) for admin_id in tg_bot.get("admins").split(",")
    ]
    return BotConfig(token=tg_bot.get("token"), admins_id=admins_list)
