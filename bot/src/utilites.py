import os
import json


def append_message(folder: str, filename: str, msg: dict) -> None:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    temp_dict = {}
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            temp_dict = json.load(f)

    temp_dict.update(msg)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(temp_dict, f, ensure_ascii=False, indent=4)


def read_messages(folder: str, filename: str) -> dict:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(file_path):
        raise Exception

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            temp_dict = json.load(f)

    return temp_dict


def rewrite_messages(folder: str, filename: str, msgs: dict) -> None:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(msgs, f, ensure_ascii=False, indent=4)
