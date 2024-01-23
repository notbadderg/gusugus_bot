import requests


class TelegramBot:
    def __init__(self, api_root, token, allowed_users, channel_id):
        self.api_root = api_root
        self.token = token
        self.allowed_users = allowed_users
        self.channel_id = channel_id

        self.request_root = self.api_root + self.token

    def send_msg(self, message):
        method = '/sendMessage'
        url = self.request_root + method

        try:
            response = requests.post(url, json={'chat_id': self.channel_id, 'text': message})
            return response
        except Exception as e:
            print(e)
