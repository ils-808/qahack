from pathlib import Path


def get_path(file_name):
    path = Path(__file__).parent.joinpath(f"{file_name}")
    print(f"get_path resolved file path: {path}")
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
