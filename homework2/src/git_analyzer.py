import os
import zlib

def read_git_object(repo_path, object_hash):
    """Чтение объекта из .git/objects."""
    obj_path = os.path.join(repo_path, ".git", "objects", object_hash[:2], object_hash[2:])
    try:
        with open(obj_path, "rb") as file:
            compressed_data = file.read()
        return zlib.decompress(compressed_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Объект {object_hash} не найден в репозитории.")

def parse_commit_object(data):
    """Парсинг объекта коммита."""
    content = data.split(b'\x00', 1)[1].decode()
    lines = content.splitlines()
    parents = [line.split()[1] for line in lines if line.startswith("parent")]
    message = lines[lines.index("") + 1:]  # Сообщение коммита
    return parents, " ".join(message)

def get_commit_by_tag(repo_path, tag_name):
    """Получение хеша коммита для указанного тега."""
    tag_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if os.path.exists(tag_path):
        with open(tag_path, "r") as file:
            return file.read().strip()
    # Если теги упакованы
    packed_refs_path = os.path.join(repo_path, ".git", "packed-refs")
    if os.path.exists(packed_refs_path):
        with open(packed_refs_path, "r") as file:
            for line in file:
                if line.strip().endswith(f"refs/tags/{tag_name}"):
                    return line.split()[0]
    raise ValueError(f"Тег {tag_name} не найден.")
