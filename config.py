import os

from dotenv import load_dotenv, find_dotenv


def get_cfg():
    load_dotenv(find_dotenv())

    params = [
        'TG_API_ROOT',
        'TG_TOKEN',
        'TG_CHANNEL_ID',
        'TG_ALLOWED_USERS',

        'DS_API_ROOT',
        'DS_TOKEN',
        'DS_CHANNEL_ID',

        'TWITCH_URL',
        'YOUTUBE_URL',
    ]
    cfg = {}

    for param in params:
        cfg[param] = os.getenv(param)

    return cfg
