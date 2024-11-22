# git_analyzer.py

import os
import subprocess


def get_commit_by_tag(repo_path, tag_name):
    """Получение хеша коммита по тегу."""
    try:
        print(f"Working directory: {os.getcwd()}")  # Отображаем текущую рабочую директорию
        result = subprocess.run(
            ['git', 'show-ref', '--tags', tag_name],
            cwd=repo_path,  # Указываем правильный путь к репозиторию
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Output from git show-ref: {result.stdout}")  # Отладочная информация

        # Извлекаем хеш коммита из строки
        ref = result.stdout.strip()
        if not ref:
            raise FileNotFoundError(f"Тег {tag_name} не найден в репозитории.")

        commit_hash = ref.split()[0]
        return commit_hash
    except subprocess.CalledProcessError:
        raise FileNotFoundError(f"Тег {tag_name} не найден в репозитории.")


def read_git_object(repo_path, object_hash):
    """Чтение git-объекта по хешу."""
    object_path = os.path.join(repo_path, ".git", "objects", object_hash[:2], object_hash[2:])
    try:
        with open(object_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Объект {object_hash} не найден в репозитории.")


def parse_commit_object(commit_data):
    """Разбор данных коммита и извлечение необходимой информации."""
    commit_lines = commit_data.decode('utf-8').split('\n')
    message = ""
    parents = []

    for line in commit_lines:
        if line.startswith("parent"):
            parents.append(line.split()[1])
        elif line.startswith("commit"):
            continue  # Пропускаем строку с хешем коммита
        else:
            message = line.strip()

    return message, parents


def get_commit_message(repo_path, commit_hash):
    """Получение сообщения коммита по хешу."""
    try:
        commit_data = read_git_object(repo_path, commit_hash)
        message, parents = parse_commit_object(commit_data)
        return message, parents
    except FileNotFoundError as e:
        print(f"Ошибка при чтении объекта {commit_hash}: {e}")
        return None, []
