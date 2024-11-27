import yaml
import os
import hashlib

def load_config(config_path):
    """Загружает конфигурационный файл."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def find_commit_hash_for_tag(repository_path, tag_name):
    """Находит хэш коммита для указанного тега."""
    try:
        ref_path = os.path.join(repository_path, '.git', 'refs', 'tags', tag_name)
        if not os.path.exists(ref_path):
            print(f"Tag {tag_name} not found in the repository.")
            return None
        with open(ref_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error finding commit hash for tag {tag_name}: {e}")
        return None

def parse_commit(commit_hash, repository_path):
    """Парсит информацию о коммите по его хэшу."""
    try:
        object_path = os.path.join(repository_path, '.git', 'objects', commit_hash[:2], commit_hash[2:])
        with open(object_path, 'rb') as file:
            content = file.read()
            # Разбираем данные объекта коммита
            commit_data = content.decode('utf-8')
            parent_hashes = []
            message = ''
            for line in commit_data.splitlines():
                if line.startswith('parent '):
                    parent_hashes.append(line.split(' ')[1])
                elif line.startswith('committer ') or line.startswith('author '):
                    continue
                else:
                    message = line
            return parent_hashes, message
    except Exception as e:
        print(f"Error parsing commit {commit_hash}: {e}")
        return [], ""

def build_dependency_graph(repository_path, tag_name):
    """Строит граф зависимостей для коммитов, начиная с тега."""
    commit_hash = find_commit_hash_for_tag(repository_path, tag_name)
    if not commit_hash:
        return []

    graph = []
    visited_commits = set()

    def process_commit(commit_hash):
        if commit_hash in visited_commits:
            return
        visited_commits.add(commit_hash)

        parent_hashes, message = parse_commit(commit_hash, repository_path)
        for parent_hash in parent_hashes:
            graph.append((commit_hash, parent_hash, message))
            process_commit(parent_hash)

    # Начинаем с коммита, связанного с тегом
    process_commit(commit_hash)
    return graph

def generate_plantuml(graph, output_file):
    """Генерирует код PlantUML для графа зависимостей."""
    plantuml_code = '@startuml\n'
    plantuml_code += 'top to bottom direction\n'  # Добавляем вертикальное расположение узлов

    for parent, child, message in graph:
        plantuml_code += f'"{child}\n{message}" --> "{parent}"\n'

    plantuml_code += '@enduml'

    try:
        with open(output_file, 'w') as file:
            file.write(plantuml_code)
        print(f"Dependency graph saved in '{output_file}'")
    except IOError as e:
        print(f"Error writing PlantUML file: {e}")

def main():
    config_path = '../config/config.yaml'

    config = load_config(config_path)
    if not config:
        return

    # Извлекаем параметры из конфигурации
    visualization_tool_path = config.get('visualization_tool_path')
    repository_path = config.get('repository_path')
    output_file = config.get('output_file_path')
    tag_name = config.get('tag_name')

    if not all([visualization_tool_path, repository_path, output_file, tag_name]):
        print("Invalid configuration, missing required parameters.")
        return

    # Строим граф зависимостей
    graph = build_dependency_graph(repository_path, tag_name)
    if graph:
        print("Final Graph:", graph)
        generate_plantuml(graph, output_file)

if __name__ == "__main__":
    main()
