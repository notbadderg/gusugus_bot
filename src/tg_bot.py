import requests
import time

from src.utilites import append_message, read_messages, rewrite_messages


class TelegramBot:
    def __init__(self, cfg, msgs):
        self.api_root = cfg['TG_API_ROOT']
        self.token = cfg['TG_TOKEN']
        self.allowed_users = cfg['TG_ALLOWED_USERS']
        self.channel_id = int(cfg['TG_CHANNEL_ID'])

        self.temp_file = cfg['TG_TEMP_FILE']
        self.temp_folder = cfg['TEMP_FOLDER']

        self.msgs = msgs

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
                result = response.json()['result']
                buffered_message = {result['message_id']: result['text']}
                append_message(self.temp_folder, self.temp_file, buffered_message)
            return response
        except Exception as e:
            print(e)

    def finish_announce(self):
        method = '/editMessageText'
        url = self.request_root + method

        body = {
            'disable_web_page_preview': True,
            'chat_id': self.channel_id,
            'parse_mode': 'html',
        }

        buffered_messages = read_messages(self.temp_folder, self.temp_file)

        bad_messages = {}
        for id_, text in buffered_messages.items():
            if self.msgs.satellite not in text or self.msgs.green_check in text:
                bad_messages[id_] = text
                continue
            old_text = text.split(self.msgs.satellite)[-1].split('https')[0]

            body.update({
                'text': f'{self.msgs.stream_ended_string()}<del>{old_text}</del>',
                'message_id': id_
            })

            response = requests.post(url, json=body)
            print(response)
            if response.status_code != 200:
                bad_messages[id_] = text
            time.sleep(0.5)

        rewrite_messages(self.temp_folder, self.temp_file, bad_messages)



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

