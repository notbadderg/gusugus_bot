class CustomMessages:
    def __init__(self, twitch_url, youtube_url):
        self.twitch_url = twitch_url
        self.youtube_url = youtube_url

        self.warning_sign = '\u26a0\ufe0f'
        self.satellite = '\ud83d\udce1'
        self.green_check = '\u2705'
        self.blue_info = '\u2139\ufe0f'

    def stream_ended_string(self):
        str_ = f'{self.green_check} Стрим завершен.\n'
        return str_

    def stream_only_twitch_string(self):
        str_ = (f'{self.warning_sign} Трансляция будет только на Twitch!\n'
                f'\n'
                f'{self.twitch_url}\n')
        return str_

    def stream_everywhere_string(self):
        str_ = (f'{self.blue_info} Трансляция будет на Twitch и на YouTube.\n'
                f'\n'
                f'{self.twitch_url}\n'
                f'{self.youtube_url}\n')
        return str_
