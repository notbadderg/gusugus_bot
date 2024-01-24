from config import get_cfg
from src.tg_bot import TelegramBot
from src.ds_bot import DiscordBot

from src.messages import CustomMessages


def main():
    cfg = get_cfg()
    msgs = CustomMessages(cfg['TWITCH_URL'], cfg['YOUTUBE_URL'])

    ds_bot = DiscordBot(cfg, msgs)
    tg_bot = TelegramBot(cfg, msgs, ds_bot)

    tg_bot.start()


if __name__ == '__main__':
    main()
