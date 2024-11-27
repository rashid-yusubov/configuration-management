import yaml
import os
import zlib


def read_config(config_path):
    """
    Чтение конфигурационного файла YAML.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def read_tag_commit(repo_path, tag_name):
    """
    Чтение хэша коммита, соответствующего заданному тегу.
    """
    tags_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    try:
        with open(tags_path, 'r') as file:
            commit_hash = file.read().strip()
            print(f"Found commit hash for tag {tag_name}: {commit_hash}")
            return commit_hash
    except FileNotFoundError:
        raise FileNotFoundError(f"Tag file not found: {tags_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {tags_path}")


def read_git_object(repo_path, obj_hash):
    """
    Чтение объекта из папки .git/objects по его хэшу.
    """
    objects_path = os.path.join(repo_path, ".git", "objects", obj_hash[:2], obj_hash[2:])
    print(f"Reading object at: {objects_path}")
    try:
        with open(objects_path, 'rb') as file:
            compressed_data = file.read()
            data = zlib.decompress(compressed_data).decode('utf-8')
            print(f"Object {obj_hash} content:\n{data}")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Git object not found: {objects_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {objects_path}")
    except zlib.error as e:
        raise ValueError(f"Error decompressing object {obj_hash}: {e}")


def parse_commit(commit_content):
    """
    Разбор содержимого объекта коммита.
    """
    lines = commit_content.split("\n")
    parents = [line.split()[1] for line in lines if line.startswith("parent")]
    message_index = lines.index('') + 1 if '' in lines else len(lines)
    message = " ".join(lines[message_index:]).strip()
    print(f"Parsed commit: parents={parents}, message='{message}'")
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
        print(f"Processing commit: {commit_hash}")
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
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(output_file, 'w') as file:
            file.write("@startuml\n")
            for node, parent, message in graph:
                file.write(f'"{node}\\n{message}" --> "{parent}"\n')
            file.write("@enduml\n")
    except FileNotFoundError:
        raise FileNotFoundError(f"Output file not found: {output_file}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {output_file}")
    except Exception as e:
        raise IOError(f"Error writing to file {output_file}: {e}")


if __name__ == "__main__":
    try:
        # Шаг 1: Чтение конфигурации
        config_path = "../config/config.yaml"
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

    except Exception as e:
        print(f"Error: {e}")
