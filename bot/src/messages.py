class CustomMessages:
    def __init__(self, twitch_url, youtube_url):
        self.twitch_url = twitch_url
        self.youtube_url = youtube_url

        self.warning_sign = '⚠️'
        self.satellite = '📡'
        self.green_check = '✅'
        self.blue_info = 'ℹ️'
        self.red_circle = '⭕️'

        self.warning = ('=====\n🚧🧀🪿🚧')
                        
    def stream_finished_string(self):
        str_ = f'{self.green_check} Стрим завершен.\n'
        return str_

    def stream_aborted_string(self):
        str_ = f'{self.red_circle} Анонс отменен. \n'
        return str_

    def stream_only_twitch_string(self):
        str_ = (f'{self.warning_sign} Трансляция будет только на Twitch!\n'
                f'\n'
                f'{self.twitch_url}\n')
        return str_

    def stream_everywhere_string(self):
        str_ = (f'{self.blue_info} Трансляция будет на Twitch и на YouTube.\n'
                f'\n'
                f'{self.twitch_url}\n\n'
                f'{self.youtube_url}\n')
        return str_

    def stream_starts_soon(self):
        str_ = f'{self.satellite} Скоро начнется стрим!\n'
        return str_
