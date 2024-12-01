from pathlib import Path


def get_path(file_name):
    return str(Path(__file__).parent.joinpath(f"{file_name}"))


def prepare_file(file_name):
    """
    Подготавливает файл для загрузки.

    :param file_name: Имя файла для загрузки.
    :return: Кортеж с параметрами для передачи файла.
    """
    file_path = get_path(file_name)
    print(f"Preparing file: {file_path}")
    with open(file_path, 'rb') as file:  # Открываем файл в бинарном режиме
        file_contents = file.read()  # Читаем содержимое файла
    return file_contents
