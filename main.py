import json

from config import get_cfg
from src.tg_bot import TelegramBot
from src.ds_bot import DiscordBot

from src.messages import CustomMessages


# "content": "sattelite:\ud83d\udce1 ... okay:\u2705  ... warning:\u26a0\ufe0f",


def main():

    cfg = get_cfg()
    msg = CustomMessages(cfg['TWITCH_URL'], cfg['YOUTUBE_URL'])


    # Test
    tg_bot = TelegramBot(cfg['TG_API_ROOT'], cfg['TG_TOKEN'], cfg['TG_ALLOWED_USERS'], cfg['TG_CHANNEL_ID'])
    response = tg_bot.send_msg(msg.stream_everywhere())
    print(f'{response.status_code}: {response.text}')

    ds_bot = DiscordBot(cfg['DS_API_ROOT'], cfg['DS_TOKEN'], cfg['DS_CHANNEL_ID'])
    # # response = ds_bot.send_msg('\u2705')
    response = ds_bot.get_msgs()
    print(f'{response.status_code}: {response.text}')
    pretty_response = json.dumps(response.json(), indent=4)

    print(pretty_response)


if __name__ == '__main__':
    main()
