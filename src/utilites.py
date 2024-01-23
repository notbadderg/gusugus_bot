import os


def append_id(folder: str, filename: str, id_: str) -> None:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    with open(file_path, 'a') as f:
        f.write(f'{id_}\n')


def read_ids(folder: str, filename: str) -> set:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(file_path):
        raise Exception

    with open(file_path, 'r') as f:
        raw_lines = f.readlines()

    ids = set([int(line) for line in raw_lines])
    print(ids)
    return ids


def rewrite_ids(folder: str, filename: str, ids: set) -> None:
    tmp_folder_path = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(tmp_folder_path, filename)

    if not os.path.exists(tmp_folder_path):
        os.mkdir(tmp_folder_path)

    with open(file_path, 'w') as f:
        for id_ in ids:
            f.write(f'{id_}\n')
