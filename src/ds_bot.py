import requests


class DiscordBot:
    def __init__(self, api_root, token, channel_id):
        self.api_root = api_root
        self.token = token
        self.channel_id = channel_id

        self.request_url = f'{self.api_root}//channels/{self.channel_id}//messages'
        self.headers = {
            'ContentType': 'application/json',
            'Authorization': f'Bot {self.token}',
            'User-Agent': 'bot testing',
        }

    def send_msg(self, message):

        body = {
            'content': message
        }

        try:
            response = requests.post(self.request_url, headers=self.headers, data=body)
            return response
        except Exception as e:
            print(e)

    def get_msgs(self):

        try:
            response = requests.get(self.request_url, headers=self.headers)
            return response
        except Exception as e:
            print(e)


