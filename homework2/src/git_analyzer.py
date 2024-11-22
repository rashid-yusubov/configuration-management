import os
import zlib


def read_commit_object(repo_path, sha1):
    """
    Чтение объекта коммита из репозитория Git.
    """
    # Разделяем SHA1 на два компонента
    object_dir = sha1[:2]
    object_file = sha1[2:]

    object_path = os.path.join(repo_path, ".git", "objects", object_dir, object_file)
    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Commit object {sha1} not found.")

    with open(object_path, "rb") as f:
        compressed_data = f.read()
        data = zlib.decompress(compressed_data[4:])  # Игнорируем первые 4 байта (long header)
    return data.decode("utf-8")


def parse_commit_data(commit_data):
    """
    Разбирает данные коммита в Git и возвращает родительские SHA1 и сообщение.
    """
    parents = []
    message = ""
    lines = commit_data.splitlines()

    for line in lines:
        if line.startswith("parent "):
            parents.append(line[7:])
        elif line.startswith("author ") or line.startswith("committer "):
            continue  # Пропускаем авторов и коммиттеров
        elif message == "":
            message = line
        else:
            message += "\n" + line
    return parents, message


def get_commit_data(repo_path, tag_name):
    """
    Получаем SHA1 коммита для указанного тега и извлекаем данные о коммитах.
    """
    tag_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if not os.path.exists(tag_path):
        raise FileNotFoundError(f"Tag {tag_name} not found.")

    with open(tag_path, "r") as f:
        start_sha1 = f.read().strip()

    commits = []
    visited = set()
    stack = [start_sha1]

    while stack:
        sha1 = stack.pop()
        if sha1 in visited:
            continue
        visited.add(sha1)

        commit_data = read_commit_object(repo_path, sha1)
        parents, message = parse_commit_data(commit_data)
        commits.append({"sha1": sha1, "message": message})
        stack.extend(parents)  # Добавляем родительские коммиты

    return commits
