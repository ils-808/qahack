from pathlib import Path


def get_path(file_name):
    print(f"File path: {str(Path.cwd().joinpath(f"{file_name}"))}")
    return str(Path.cwd().joinpath(f"{file_name}"))


def prepare_file(file_name, file_type):
    """
    Подготавливает файл для загрузки.

    :param file_name: Имя файла для загрузки.
    :param file_type: MIME-тип файла.
    :return: Кортеж с параметрами для передачи файла.
    """
    file_path = get_path(file_name)
    print(f"File path: {file_path}")
    return [
        ('avatar_file', (file_name, open(file_path, 'rb'), file_type))
    ]
