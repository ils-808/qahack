from pathlib import Path
import os
# Получение корня проекта (например, где находится `pytest.ini` или `.git` папка)
PROJECT_ROOT = Path(__file__).resolve().parent


def get_path(file_name):
    """
    Генерирует абсолютный путь к файлу относительно корня проекта.
    """
    #file_path = PROJECT_ROOT / file_name
    file_path = os.path.join(PROJECT_ROOT,file_name)
    print(f"File path: {file_path}")
    return str(file_path)


def prepare_file(file_name, file_type):
    """
    Подготавливает файл для загрузки.

    :param file_name: Имя файла для загрузки.
    :param file_type: MIME-тип файла.
    :return: Кортеж с параметрами для передачи файла.
    """
    file_path = get_path(file_name)
    print(f"Preparing file: {file_path}")
    return [
        ('avatar_file', (file_name, open(file_path, 'rb'), file_type))
    ]
