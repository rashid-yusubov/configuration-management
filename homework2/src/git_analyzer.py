import os
import zlib
import io


def get_commit_by_tag(repo_path, tag_name):
    """Получение хеша коммита по имени тега."""
    ref_path = os.path.join(repo_path, '.git', 'refs', 'tags', tag_name)
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f"Тег {tag_name} не найден в репозитории.")

    with open(ref_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def read_git_object(repo_path, object_hash):
    """Чтение объекта из репозитория Git."""
    object_path = os.path.join(repo_path, '.git', 'objects', object_hash[:2], object_hash[2:])
    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Объект {object_hash} не найден в репозитории.")

    with open(object_path, "rb") as file:
        file_content = file.read()

    return zlib.decompress(file_content)


def parse_commit_object(data):
    """Парсинг коммита Git."""
    # Декодируем данные коммита
    stream = io.BytesIO(data)
    header = stream.read(4)  # Должен быть заголовок объекта
    if header != b'commit':
        raise ValueError("Неверный объект Git.")

    message = b""
    parents = []
    while True:
        line = stream.readline().strip()
        if line.startswith(b'parent'):
            parents.append(line.split(b' ')[1].decode())
        elif line.startswith(b''):
            break  # Переходим к сообщению коммита
        message += line + b'\n'

    return parents, message.decode().strip()
