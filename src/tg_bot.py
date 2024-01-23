import requests


class TelegramBot:
    def __init__(self, tg_token, tg_allowed_users, tg_channel_id):
        self.tg_token = tg_token
        self.tg_allowed_users = tg_allowed_users
        self.tg_channel_id = tg_channel_id
        self.api_root = f'https://api.telegram.org/bot{self.tg_token}'

    def send_msg(self, message):
        method = '/sendMessage'
        url = self.api_root + method

        try:
            response = requests.post(url, json={'chat_id': self.tg_channel_id, 'text': message})
            return response
        except Exception as e:
            print(e)
