import yaml
import os
import zlib

def read_config(config_path):
    """
    Чтение конфигурационного файла YAML.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def read_tag_commit(repo_path, tag_name):
    """
    Чтение хэша коммита, соответствующего заданному тегу.
    """
    tags_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if not os.path.exists(tags_path):
        raise FileNotFoundError(f"Tag '{tag_name}' not found.")
    with open(tags_path, 'r') as file:
        commit_hash = file.read().strip()
    return commit_hash


def read_git_object(repo_path, obj_hash):
    """
    Чтение объекта из папки .git/objects по его хэшу.
    """
    objects_path = os.path.join(repo_path, ".git", "objects", obj_hash[:2], obj_hash[2:])
    if not os.path.exists(objects_path):
        raise FileNotFoundError(f"Object '{obj_hash}' not found.")
    with open(objects_path, 'rb') as file:
        compressed_data = file.read()
    return zlib.decompress(compressed_data).decode('utf-8')


def parse_commit(commit_content):
    """
    Разбор содержимого объекта коммита.
    """
    lines = commit_content.split("\n")
    parents = [line.split()[1] for line in lines if line.startswith("parent")]
    message_index = lines.index('') + 1 if '' in lines else len(lines)
    message = " ".join(lines[message_index:]).strip()
    return parents, message


def build_dependency_graph(repo_path, start_commit):
    """
    Построение графа зависимостей для всех коммитов, начиная с указанного.
    """
    graph = []
    visited = set()

    def dfs(commit_hash):
        if commit_hash in visited:
            return
        visited.add(commit_hash)
        commit_content = read_git_object(repo_path, commit_hash)
        parents, message = parse_commit(commit_content)
        for parent in parents:
            graph.append((commit_hash, parent, message))
            dfs(parent)

    dfs(start_commit)
    return graph


def generate_plantuml(graph, output_file):
    """
    Генерация PlantUML кода для графа зависимостей.
    """
    with open(output_file, 'w') as file:
        file.write("@startuml\n")
        for node, parent, message in graph:
            file.write(f'"{node}\\n{message}" --> "{parent}"\n')
        file.write("@enduml\n")


if __name__ == "__main__":
    # Шаг 1: Чтение конфигурации
    config_path = '../config/config.yaml'
    config = read_config(config_path)

    repo_path = config['repository_path']
    tag_name = config['tag_name']
    output_file = config['output_file_path']

    # Шаг 2: Получение стартового коммита
    start_commit = read_tag_commit(repo_path, tag_name)

    # Шаг 3: Построение графа зависимостей
    graph = build_dependency_graph(repo_path, start_commit)

    # Шаг 4: Генерация PlantUML
    generate_plantuml(graph, output_file)

    print(f"Dependency graph generated in '{output_file}'")
