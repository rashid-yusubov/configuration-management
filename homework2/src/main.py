import os
import yaml


def read_config(config_path):
    """
    Чтение конфигурационного файла YAML.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")


def read_git_object(repo_path, object_hash):
    """
    Чтение объекта Git из папки .git/objects.
    """
    object_path = os.path.join(repo_path, ".git", "objects", object_hash[:2], object_hash[2:])
    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Git object not found: {object_path}")
    print(f"Reading object at: {object_path}")
    with open(object_path, 'rb') as file:
        content = file.read()
    return decompress_object(content)


def decompress_object(data):
    """
    Распаковка объекта Git.
    """
    import zlib
    return zlib.decompress(data).decode('utf-8')


def parse_commit(commit_content):
    """
    Разбор содержимого коммита Git.
    """
    lines = commit_content.split('\n')
    parents = [line.split(' ')[1] for line in lines if line.startswith('parent')]
    message_index = lines.index('') + 1
    message = '\n'.join(lines[message_index:]).strip()
    return parents, message


def build_dependency_graph(repo_path, start_commit):
    """
    Построение графа зависимостей коммитов.
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
        print(f"Commit {commit_hash} has parents: {parents}, message: '{message}'")
        for parent in parents:
            graph.append((commit_hash, parent, message))
            dfs(parent)

    dfs(start_commit)
    print("Final Graph:", graph)
    return graph


def generate_plantuml(graph, output_file):
    """
    Генерация кода PlantUML на основе графа зависимостей.
    """
    print(f"Generating PlantUML file: {output_file}")
    try:
        with open(output_file, 'w') as file:
            file.write("@startuml\n")
            for child, parent, message in graph:
                file.write(f'"{child}\\n{message}" --> "{parent}\\n"\n')
            file.write("@enduml\n")
        print(f"Dependency graph saved in '{output_file}'")
    except FileNotFoundError:
        print(f"Error: File {output_file} not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def find_commit_hash_by_tag(repo_path, tag_name):
    """
    Нахождение хэша коммита, связанного с указанным тегом.
    """
    refs_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if not os.path.exists(refs_path):
        raise FileNotFoundError(f"Tag '{tag_name}' not found in repository.")
    with open(refs_path, 'r') as file:
        commit_hash = file.read().strip()
    print(f"Found commit hash for tag {tag_name}: {commit_hash}")
    return commit_hash


if __name__ == "__main__":
    config_path = "../config/config.yaml"  # Путь к конфигурационному файлу

    try:
        config = read_config(config_path)
        visualization_tool_path = config['visualization_tool_path']
        repository_path = config['repository_path']
        output_file = config['output_file_path']
        tag_name = config['tag_name']

        # Нахождение хэша коммита по тегу
        start_commit = find_commit_hash_by_tag(repository_path, tag_name)

        # Построение графа зависимостей
        dependency_graph = build_dependency_graph(repository_path, start_commit)

        # Генерация файла PlantUML
        generate_plantuml(dependency_graph, output_file)

    except Exception as e:
        print(f"Error: {e}")
