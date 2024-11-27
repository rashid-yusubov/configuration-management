import os
import yaml
import logging


def setup_logging(log_file):
    """
    Настройка логирования.
    """
    logging.basicConfig(
        filename=log_file,  # Путь к файлу для записи логов
        level=logging.DEBUG,  # Уровень логирования (DEBUG - для отладочной информации)
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


def find_latest_commit(repo_path):
    """
    Нахождение хэша последнего коммита в ветке master.
    """
    head_path = os.path.join(repo_path, ".git", "refs", "heads", "master")
    if not os.path.exists(head_path):
        logging.error("Branch 'master' not found.")
        raise FileNotFoundError("Branch 'master' not found.")
    with open(head_path, 'r') as file:
        commit_hash = file.read().strip()
    logging.debug(f"Found latest commit hash: {commit_hash}")
    return commit_hash


if __name__ == "__main__":
    config_path = "../config/config.yaml"  # Путь к конфигурационному файлу
    log_file = "../config/app.log"  # Путь к файлу логов

    # Настройка логирования
    setup_logging(log_file)

    try:
        config = read_config(config_path)
        visualization_tool_path = config['visualization_tool_path']
        repository_path = config['repository_path']
        output_file = config['output_file_path']

        # Нахождение хэша последнего коммита
        start_commit = find_latest_commit(repository_path)

        # Построение графа зависимостей
        dependency_graph = build_dependency_graph(repository_path, start_commit)

        # Генерация и вывод кода PlantUML на экран и запись в файл
        generate_plantuml(dependency_graph, output_file)

    except Exception as e:
        logging.error(f"Error: {e}")
