import os

import requests
import time
import datetime

from src.utilites import append_message, read_messages, rewrite_messages


class TelegramBot:
    def __init__(self, cfg, msgs, ds_bot):
        self.api_root = cfg['TG_API_ROOT']
        self.token = cfg['TG_TOKEN']
        self.allowed_users = cfg['TG_ALLOWED_USERS'].split(',')
        self.channel_id = int(cfg['TG_CHANNEL_ID'])

        self.temp_file = cfg['TG_TEMP_FILE']
        self.temp_folder = cfg['TEMP_FOLDER']

        self.msgs = msgs
        self.ds_bot = ds_bot

        self.request_root = self.api_root + self.token

    def send_service_msg(self, message):
        method = '/sendMessage'
        url = self.request_root + method

        for user in self.allowed_users:

            body = {
                'disable_web_page_preview': True,
                'chat_id': user,
                'text': message,
            }

            try:
                response = requests.post(url, json=body)
                return response
            except Exception as e:
                print(e)

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
        codes = []
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
            codes.append(response.status_code)
            if response.status_code != 200:
                bad_messages[id_] = text
            time.sleep(2)

        rewrite_messages(self.temp_folder, self.temp_file, bad_messages)
        return codes

    def bot_commands(self, command):
        match command:
            case 'a':
                return 'a'
            case '/soon_all':
                message = self.msgs.stream_starts_soon() + self.msgs.stream_everywhere_string()
                r1 = self.send_msg(message).status_code
                r2 = self.ds_bot.send_msg(message).status_code
                return f'{r1}, {r2}'

            case '/finish':
                r1 = self.finish_announce()
                r2 = self.ds_bot.finish_announce()
                return f'{r1}, {r2}'

            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                return 'Unrecognized'

    def commands_switch(self, command):
        if command[0] == '/':
            return 'uwu'

        else:
            return 'UNRECOGNIZED'


    def start(self):
        bot_start_time = time.time()
        start_msg = f'{datetime.datetime.fromtimestamp(bot_start_time).strftime('%Y-%m-%d %H:%M:%S')} - start'
        print(start_msg)
        self.send_service_msg(start_msg)

        time_threshold = bot_start_time
        while True:
            time.sleep(5)

            method = '/getUpdates'
            url = self.request_root + method
            response = requests.get(url)
            print(f'{datetime.datetime.now()} - {response.status_code}')
            if response.status_code != 200:
                print('retrying in 60 secs...')
                time.sleep(60)
                continue

            raw_results = response.json()['result']
            results = sorted(raw_results, key=lambda x: x['update_id'], reverse=True)

            for result in results:

                if time_threshold >= result['message']['date']:
                    continue

                update_id = result['update_id']
                sender_id = result['message']['from']['id']
                sender_type = result['message']['from']['is_bot']
                sender_username = result['message']['from']['username']
                message_raw_date = result['message']['date']
                message_date = datetime.datetime.fromtimestamp(result['message']['date']).strftime('%Y-%m-%d %H:%M:%S')
                message_text = result['message']['text']
                log_string = f'{message_date} - {update_id} - {sender_id} {sender_type} {sender_username}: {message_text}'
                print(log_string, end='')
                if not (sender_username in self.allowed_users or str(sender_id) in self.allowed_users):
                    danger = ' ! UNAUTHORIZED ATTEMPT ! '
                    print(danger)
                    self.send_service_msg(log_string + danger)
                    continue

                print()
                result = self.commands_switch(message_text)

                log_string = (f'{message_date} - {update_id} - {sender_id} {sender_type} {sender_username}: '
                              f'RESULT {result}')
                self.send_service_msg(log_string)
                print(log_string)

                # NEED FOR COMPLETING ONLY LAST CMD
                time_threshold = time.time()
                break
            else:
                time_threshold = time.time()


