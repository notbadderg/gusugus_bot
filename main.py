import os

from dotenv import load_dotenv, find_dotenv

from src.tg_bot import TelegramBot
from src.ds_bot import DiscordBot


def main():
    load_dotenv(find_dotenv())

    tg_api_root = os.getenv('TG_API_ROOT')
    tg_token = os.getenv('TG_TOKEN')
    tg_allowed_users = os.getenv('TG_ALLOWED_USERS')
    tg_channel_id = os.getenv('TG_CHANNEL_ID')

    ds_api_root = os.getenv('DS_API_ROOT')
    ds_token = os.getenv('DS_TOKEN')
    ds_channel_id = os.getenv('DS_CHANNEL_ID')

    # Test
    # tg_bot = TelegramBot(tg_api_root, tg_token, tg_allowed_users, tg_channel_id)
    # response = tg_bot.send_msg('qweqwe')
    # print(f'{response.status_code}: {response.text}')

    ds_bot = DiscordBot(ds_api_root, ds_token, ds_channel_id)
    # response = ds_bot.send_msg('qweqwe')
    response = ds_bot.get_msgs()
    print(f'{response.status_code}: {response.text}')


if __name__ == '__main__':
    main()
