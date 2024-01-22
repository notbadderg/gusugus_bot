import os
import requests

from dotenv import load_dotenv, find_dotenv


class TelegramBot:
    def __init__(self, tg_token, tg_allowed_users, tg_channel_id):
        self.tg_token = tg_token
        self.tg_allowed_users = tg_allowed_users
        self.tg_channel_id = tg_channel_id

    def send_msg(self, message):
        api_url = f'https://api.telegram.org/bot{self.tg_token}/sendMessage'

        try:
            response = requests.post(api_url, json={'chat_id': self.tg_channel_id, 'text': message})
            return response
        except Exception as e:
            print(e)


def main():
    load_dotenv(find_dotenv())

    tg_token = os.getenv('TG_TOKEN')
    ds_token = os.getenv('DS_TOKEN')
    tg_allowed_users = os.getenv('TG_ALLOWED_USERS')
    tg_channel_id = os.getenv('TG_CHANNEL_ID')

    tg_bot = TelegramBot(tg_token, tg_allowed_users, tg_channel_id)
    response = tg_bot.send_msg('qweqwe')
    print(f'{response.status_code}: {response.text}')


if __name__ == '__main__':
    main()
