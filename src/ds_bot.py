import requests
import time

from src.utilites import append_message, read_messages, rewrite_messages


class DiscordBot:
    def __init__(self, cfg, msgs):
        self.api_root = cfg['DS_API_ROOT']
        self.token = cfg['DS_TOKEN']
        self.channel_id = cfg['DS_CHANNEL_ID']

        self.temp_file = cfg['DS_TEMP_FILE']
        self.temp_folder = cfg['TEMP_FOLDER']

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
            if response.status_code == 200:
                # print(response.json())
                result = response.json()
                buffered_message = {result['id']: result['content']}
                append_message(self.temp_folder, self.temp_file, buffered_message)
            return response
        except Exception as e:
            print(e)

    def finish_announce(self):

        buffered_messages = read_messages(self.temp_folder, self.temp_file)
        codes = []
        bad_messages = {}
        for id_, text in buffered_messages.items():
            if self.msgs.satellite not in text or self.msgs.green_check in text:
                bad_messages[id_] = text
                continue
            old_content = text.split(self.msgs.satellite)[-1].split('https')[0]

            url = self.request_url + '/' + id_

            new_message = {
                'flags': '4',
                'content': f'@everyone {self.msgs.stream_ended_string()}~~{old_content}~~'
            }
            try:
                response = requests.patch(url, headers=self.headers, data=new_message)
                codes.append(response.status_code)
                if response.status_code != 200:
                    bad_messages[id_] = text
                time.sleep(2)
            except Exception as e:
                print(e)

        rewrite_messages(self.temp_folder, self.temp_file, bad_messages)
        return codes

    def get_msgs(self):

        try:
            response = requests.get(self.request_url, headers=self.headers)
            return response
        except Exception as e:
            print(e)


