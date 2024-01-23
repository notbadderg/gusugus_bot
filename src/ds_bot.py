import requests


class DiscordBot:
    def __init__(self, api_root, token, channel_id, msgs):
        self.api_root = api_root
        self.token = token
        self.channel_id = channel_id
        self.msgs = msgs

        self.request_url = f'{self.api_root}//channels/{self.channel_id}//messages'
        self.headers = {
            'ContentType': 'application/json',
            'Authorization': f'Bot {self.token}',
            'User-Agent': 'bot testing',
        }

    def send_msg(self, message):

        body = {
            'flags': '4',
            'content': f'@everyone {message}',
        }

        try:
            response = requests.post(self.request_url, headers=self.headers, data=body)
            return response
        except Exception as e:
            print(e)

    def finish_announce(self):
        response = requests.get(self.request_url, headers=self.headers)
        # u = response.json()
        # print(u)
        for message in response.json():
            if self.msgs.satellite in message['content']:
                old_content = message['content'].split(self.msgs.satellite)[-1].split('https')[0]

                url = self.request_url + '/' + message['id']

                new_message = {
                    'flags': '4',
                    'content': f'@everyone {self.msgs.stream_ended_string()}~~{old_content}~~'
                }
                try:
                    response = requests.patch(url, headers=self.headers, data=new_message)
                    return response
                except Exception as e:
                    print(e)

    def get_msgs(self):

        try:
            response = requests.get(self.request_url, headers=self.headers)
            return response
        except Exception as e:
            print(e)


