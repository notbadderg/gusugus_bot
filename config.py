import os

from dotenv import load_dotenv, find_dotenv


def get_cfg():
    load_dotenv(find_dotenv())

    params = [
        'TEMP_FOLDER',

        'TG_API_ROOT',
        'TG_TOKEN',
        'TG_CHANNEL_ID',
        'TG_ALLOWED_USERS',
        'TG_TEMP_FILE',
        'TG_POOL_REFRESH_TIME',

        'DS_API_ROOT',
        'DS_TOKEN',
        'DS_CHANNEL_ID',
        'DS_TEMP_FILE',

        'TWITCH_URL',
        'YOUTUBE_URL',
    ]
    cfg = {}

    for param in params:
        cfg[param] = os.getenv(param)

    return cfg
