import os
from pathlib import Path

workspace_path = os.getenv("GITHUB_WORKSPACE", "/home/runner/work/qahack/qahack")


def get_path(file_name):
    if workspace_path != "/home/runner/work/qahack/qahack/":
        print("Код выполняется на GitHub")
        return workspace_path+"/"+file_name
    else:
        path = Path(__file__).parent.joinpath(f"{file_name}")
        print(f"Код выполняется на Winodws: {path}")
        return str(path)


def prepare_file(file_name):
    """
    Подготавливает файл для загрузки.

    :param file_name: Имя файла для загрузки.
    :return: Кортеж с параметрами для передачи файла.
    """
    file_path = get_path(file_name)
    print(f"Preparing file: {file_path}")
    try:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        print(f"File read successfully: {file_name}")
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        raise
    return file_contents
