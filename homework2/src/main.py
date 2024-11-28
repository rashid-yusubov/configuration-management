import os
import yaml
import logging


def setup_logging(log_file):
    """
    Настройка логирования.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )


def read_config(config_path):
    """
    Чтение конфигурационного файла YAML.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise ValueError(f"Error parsing YAML configuration: {e}")


def read_git_object(repo_path, object_hash):
    """
    Чтение объекта Git из папки .git/objects.
    """
    object_path = os.path.join(repo_path, ".git", "objects", object_hash[:2], object_hash[2:])
    if not os.path.exists(object_path):
        logging.error(f"Git object not found: {object_path}")
        raise FileNotFoundError(f"Git object not found: {object_path}")
    logging.debug(f"Reading object at: {object_path}")
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
        logging.debug(f"Processing commit: {commit_hash}")
        commit_content = read_git_object(repo_path, commit_hash)
        parents, message = parse_commit(commit_content)
        logging.debug(f"Commit {commit_hash} has parents: {parents}, message: '{message}'")
        for parent in parents:
            graph.append((commit_hash, parent, message))
            dfs(parent)

    dfs(start_commit)
    logging.debug("Final Graph: %s", graph)
    return graph


def generate_plantuml(graph, output_file):
    """
    Генерация кода PlantUML на основе графа зависимостей,
    вывод на экран и запись в файл.
    """
    logging.debug("Generating PlantUML code")
    plantuml_code = "@startuml\n"

    # Генерация кода для графа
    for child, parent, message in graph:
        plantuml_code += f'"{child}\\n{message}" --> "{parent}\\n"\n'

    plantuml_code += "@enduml\n"

    # Выводим на экран
    print(plantuml_code)

    # Записываем в файл
    try:
        with open(output_file, 'w') as file:
            file.write(plantuml_code)
        logging.debug(f"Dependency graph saved in '{output_file}'")
    except FileNotFoundError:
        logging.error(f"Error: File {output_file} not found.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def get_commit_hash_by_tag(repo_path, tag_name):
    """
    Получение хэша коммита, связанного с тегом.
    """
    tag_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if not os.path.exists(tag_path):
        logging.error(f"Tag '{tag_name}' not found.")
        raise FileNotFoundError(f"Tag '{tag_name}' not found.")
    with open(tag_path, 'r') as file:
        commit_hash = file.read().strip()
    logging.debug(f"Found commit hash for tag '{tag_name}': {commit_hash}")
    return commit_hash


def resolve_tag_to_commit(repo_path, tag_hash):
    """
    Раскрытие аннотированного тега до хэша коммита.
    """
    tag_content = read_git_object(repo_path, tag_hash)
    if tag_content.startswith("object"):
        # Извлечь хэш коммита из аннотированного тега
        lines = tag_content.split("\n")
        for line in lines:
            if line.startswith("object"):
                return line.split(" ")[1]
    return tag_hash


if __name__ == "__main__":
    config_path = "../config/config.yaml"  # Путь к конфигурационному файлу
    log_file = "../config/app.log"  # Путь к файлу логов

    # Настройка логирования
    setup_logging(log_file)

    try:
        # Чтение конфигурации
        config = read_config(config_path)
        visualization_tool_path = config['visualization_tool_path']
        repository_path = config['repository_path']
        output_file = config['output_file_path']
        tag_name = config['tag_name']

        # Нахождение хэша коммита по тегу
        commit_hash = get_commit_hash_by_tag(repository_path, tag_name)
        start_commit = resolve_tag_to_commit(repository_path, commit_hash)

        # Построение графа зависимостей
        dependency_graph = build_dependency_graph(repository_path, start_commit)

        # Генерация и вывод кода PlantUML на экран и запись в файл
        generate_plantuml(dependency_graph, output_file)

    except Exception as e:
        logging.error(f"Error: {e}")
