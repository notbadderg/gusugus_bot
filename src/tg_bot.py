import requests
import time

from src.utilites import append_id, read_ids, rewrite_ids


class TelegramBot:
    def __init__(self, api_root, token, allowed_users, channel_id, msgs, temp_folder, tg_temp_file):
        self.api_root = api_root
        self.token = token
        self.allowed_users = allowed_users
        self.channel_id = int(channel_id)

        self.msgs = msgs
        self.temp_folder = temp_folder
        self.tg_temp_file = tg_temp_file

        self.request_root = self.api_root + self.token

    def send_msg(self, message):
        method = '/sendMessage'
        url = self.request_root + method
        body = {
            'disable_web_page_preview': True,
            'chat_id': self.channel_id,
            'text': message,
        }

        try:
            response = requests.post(url, json=body)
            if response.status_code == 200:
                message_id = response.json()['result']['message_id']
                append_id(self.temp_folder, self.tg_temp_file, message_id)
            return response
        except Exception as e:
            print(e)

    def finish_announce(self):
        # read_ids(self.temp_folder, self.tg_temp_file)
        #
        method = '/editMessageText'
        url = self.request_root + method

        body = {
            'disable_web_page_preview': True,
            'chat_id': self.channel_id,
            'text': 'asddsas',
        }

        ids = read_ids(self.temp_folder, self.tg_temp_file)

        bad_set = set()
        for id_ in ids:
            body.update({
                'message_id': id_
            })
            response = requests.post(url, json=body)
            print(response)
            if response.status_code != 200:
                bad_set.add(id_)
            time.sleep(0.5)

        rewrite_ids(self.temp_folder, self.tg_temp_file, bad_set)



        #
        #
        #
        # method = f'/getUpdates?chat_id={self.channel_id}'
        # url = self.request_root + method
        # headers = {
        #     'chat_id': self.channel_id,
        # }
        #
        # response = requests.get(url)
        # print(response.json())
        # u = response.json()
        # print(u)
        # for message in response.json():
        #     if self.msgs.satellite in message['content']:
        #         old_content = message['content'].split(self.msgs.satellite)[-1].split('https')[0]
        #
        #         url = self.request_url + '/' + message['id']
        #
        #         new_message = {
        #             'flags': '4',
        #             'content': f'@everyone {self.msgs.stream_ended_string()}~~{old_content}~~'
        #         }
        #         try:
        #             response = requests.patch(url, headers=self.headers, data=new_message)
        #             return response
        #         except Exception as e:
        #             print(e)


    def start(self):
        while True:
            pass
            method = '/getUpdates?offset=-1'
            url = self.request_root + method
            headers = {
                'chat_id': self.channel_id,
            }

            response = requests.get(url)
            print(response.json())

