import os
import yaml
import zlib


def read_config(config_path):
    """Чтение конфигурационного файла."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def get_tag_hash(repo_path, tag_name):
    """Получение хэша тега из .git/refs/tags/{tag_name}."""
    tag_path = os.path.join(repo_path, ".git", "refs", "tags", tag_name)
    if not os.path.exists(tag_path):
        raise FileNotFoundError(f"Тег {tag_name} не найден.")
    with open(tag_path, 'r') as file:
        return file.read().strip()


def read_git_object(repo_path, object_hash):
    """Чтение объекта Git из .git/objects/{prefix}/{hash}."""
    obj_dir = os.path.join(repo_path, ".git", "objects", object_hash[:2])
    obj_file = os.path.join(obj_dir, object_hash[2:])

    if not os.path.exists(obj_file):
        raise FileNotFoundError(f"Объект {object_hash} не найден.")

    with open(obj_file, 'rb') as file:
        compressed_data = file.read()
        decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data


def parse_commit_object(commit_data):
    """Разбор объекта коммита Git."""
    # Разделение заголовка и тела
    header, body = commit_data.split(b'\n\n', 1)
    headers = header.split(b'\n')

    parents = []
    message = body.decode('utf-8').strip()

    for line in headers:
        if line.startswith(b'parent'):
            parents.append(line.split(b' ')[1].decode('utf-8'))

    return parents, message


def build_dependency_graph(repo_path, start_hash):
    """Построение графа зависимостей коммитов."""
    dependencies = {}
    queue = [start_hash]
    visited = set()

    while queue:
        current_hash = queue.pop(0)
        if current_hash in visited:
            continue

        visited.add(current_hash)
        commit_data = read_git_object(repo_path, current_hash)
        parents, message = parse_commit_object(commit_data)
        dependencies[current_hash] = {
            "parents": parents,
            "message": message
        }

        queue.extend(parents)

    return dependencies


def generate_plantuml_from_dependencies(dependencies):
    """Генерация кода PlantUML из графа зависимостей."""
    lines = ["@startuml", "scale 1"]

    for commit, data in dependencies.items():
        for parent in data['parents']:
            lines.append(f'"{commit}\\n{data["message"]}" --> "{parent}"')

    lines.append("@enduml")
    return "\n".join(lines)


def save_to_file(content, file_path):
    """Сохранение содержимого в файл."""
    with open(file_path, 'w') as file:
        file.write(content)


def run_visualizer(visualizer_path, output_path):
    """Запуск программы для визуализации графа."""
    os.system(f"{visualizer_path} {output_path}")


def main(config_path):
    """Основная программа."""
    config = read_config(config_path)

    repo_path = config['repository_path']
    tag_name = config['tag_name']
    output_path = config['output_path']
    visualizer_path = config['visualizer_path']

    try:
        tag_hash = get_tag_hash(repo_path, tag_name)
        dependencies = build_dependency_graph(repo_path, tag_hash)
        plantuml_code = generate_plantuml_from_dependencies(dependencies)

        save_to_file(plantuml_code, output_path)
        print(f"Граф зависимостей сгенерирован и сохранён в {output_path}.")

        # Запуск визуализатора для генерации изображения
        run_visualizer(visualizer_path, output_path)
        print(f"Визуализация графа завершена.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Использование: python main.py <config_path>")
    else:
        main(sys.argv[1])
