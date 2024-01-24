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
        self.pool_refresh_time = float(cfg['TG_POOL_REFRESH_TIME'])

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

    def close_announce(self, reason):
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
            if self.msgs.satellite not in text or self.msgs.green_check in text or self.msgs.red_circle in text:
                bad_messages[id_] = text
                continue
            old_text = text.split(self.msgs.satellite)[-1].split('https')[0]

            if reason == 'aborted':
                msg = self.msgs.stream_aborted_string()
            elif reason == 'finished':
                msg = self.msgs.stream_finished_string()
            else:
                raise Exception

            body.update({
                'text': f'{msg}<del>{old_text}</del>',
                'message_id': id_
            })

            response = requests.post(url, json=body)
            codes.append(response.status_code)
            if response.status_code != 200:
                bad_messages[id_] = text
            time.sleep(2)

        rewrite_messages(self.temp_folder, self.temp_file, bad_messages)
        return codes

    def commands_switch(self, command):
        if command == '/start':
            cmds = ('\n'
                    '\n'
                    '/start\n\n'
                    '/finish\n\n'
                    '/abort\n\n'
                    '/soonall\n\n'
                    '/soontwi\n\n'
                    '/maall {msg}\n\n'
                    '/matwi {msg}\n\n'
                    '/maoth {msg}\n\n'
                    )
            return cmds

        elif command == '/finish':
            r1 = self.close_announce('finished')
            r2 = self.ds_bot.close_announce('finished')
            return f'{r1}, {r2}'

        elif command == '/abort':
            r1 = self.close_announce('aborted')
            r2 = self.ds_bot.close_announce('aborted')
            return f'{r1}, {r2}'

        elif command == '/soonall':
            msg = (f'{self.msgs.stream_starts_soon()}'
                   f'{self.msgs.stream_everywhere_string()}\n'
                   f'{self.msgs.warning}')
            r1 = self.send_msg(msg).status_code
            r2 = self.ds_bot.send_msg(msg).status_code
            return f'{r1}, {r2}'

        elif command == '/soontwi':
            msg = (f'{self.msgs.stream_starts_soon()}'
                   f'{self.msgs.stream_only_twitch_string()}\n'
                   f'{self.msgs.warning}')
            r1 = self.send_msg(msg).status_code
            r2 = self.ds_bot.send_msg(msg).status_code
            return f'{r1}, {r2}'

        elif command[:3] == '/ma':
            command = command[3:]
            if len(command) < 10:
                msg = 'too short cmd'
                return msg

            elif command[:3] == 'all':
                msg = (f'{self.msgs.satellite} {command[4:]}\n'
                       f'{self.msgs.stream_everywhere_string()}\n'
                       f'{self.msgs.warning}')
                r1 = self.send_msg(msg).status_code
                r2 = self.ds_bot.send_msg(msg).status_code
                return f'{msg}\n{r1}, {r2}'

            elif command[:3] == 'twi':
                msg = (f'{self.msgs.satellite} {command[4:]}\n'
                       f'{self.msgs.stream_only_twitch_string()}\n'
                       f'{self.msgs.warning}')
                r1 = self.send_msg(msg).status_code
                r2 = self.ds_bot.send_msg(msg).status_code
                return f'{msg}\n{r1}, {r2}'

            elif command[:3] == 'oth':
                msg = (f'{self.msgs.blue_info} {command[4:]}\n\n'
                       f'{self.msgs.warning}')
                r1 = self.send_msg(msg).status_code
                r2 = self.ds_bot.send_msg(msg).status_code
                return f'{msg}\n{r1}, {r2}'

        return 'UNRECOGNIZED'

    def start(self):
        bot_start_time = time.time()
        start_msg = f'{datetime.datetime.fromtimestamp(bot_start_time).strftime('%Y-%m-%d %H:%M:%S')} - /start'
        print(start_msg)
        self.send_service_msg(start_msg)

        processed_messages = []
        confirms_count = 0
        prev_cmd = 'uwu'
        while True:
            if len(processed_messages) > 80:
                processed_messages = processed_messages[50:]

            time.sleep(self.pool_refresh_time)
            body = {
                "offset": -10,
                "limit": 50,
                "timeout": 0,
            }
            method = '/getUpdates'
            url = self.request_root + method
            response = requests.post(url, json=body)
            print(f'{datetime.datetime.now()} - {response.status_code}')
            if response.status_code != 200:
                print('retrying in 60 secs...')
                time.sleep(60)
                continue

            raw_results = response.json()['result']
            results = sorted(raw_results, key=lambda x: x['update_id'], reverse=True)
            for result in results:

                update_id = result['update_id']
                if bot_start_time >= result['message']['date'] or update_id in processed_messages:
                    continue

                sender_id = result['message']['from']['id']
                sender_type = result['message']['from']['is_bot']
                sender_username = result['message']['from']['username']
                message_date = datetime.datetime.fromtimestamp(result['message']['date']).strftime('%Y-%m-%d %H:%M:%S')
                message_text = result['message']['text']
                log_string = (f'{message_date} - {update_id} - '
                              f'{sender_id} {sender_type} {sender_username}: {message_text}')
                print(log_string, end='')
                if not (sender_username in self.allowed_users or str(sender_id) in self.allowed_users):
                    danger = ' ! UNAUTHORIZED ATTEMPT ! '
                    print(danger)
                    self.send_service_msg(log_string + danger)
                    processed_messages.append(update_id)
                    continue

                print()
                if message_text != '/start' and prev_cmd == message_text:
                    confirms_count += 1
                else:
                    prev_cmd = message_text

                if message_text == '/start' or confirms_count > 0:
                    result_cmd = self.commands_switch(message_text)
                    confirms_count = 0
                    prev_cmd = 'baw'

                else:
                    result_cmd = 'Enter again for confirm'

                log_string = (f'/start {message_date} - {sender_username}: '
                              f'RESULT of {message_text}:\n{result_cmd}')
                self.send_service_msg(log_string)
                print(log_string)

                processed_messages.append(update_id)
                # NEED FOR COMPLETING ONLY LAST CMD
                break
