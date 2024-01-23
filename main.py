import os

from dotenv import load_dotenv, find_dotenv

from src.tg_bot import TelegramBot


def main():
    load_dotenv(find_dotenv())

    tg_token = os.getenv('TG_TOKEN')
    ds_token = os.getenv('DS_TOKEN')
    tg_allowed_users = os.getenv('TG_ALLOWED_USERS')
    tg_channel_id = os.getenv('TG_CHANNEL_ID')

    # Test
    tg_bot = TelegramBot(tg_token, tg_allowed_users, tg_channel_id)
    response = tg_bot.send_msg('qweqwe')
    print(f'{response.status_code}: {response.text}')


if __name__ == '__main__':
    main()
