import os
import subprocess
import yaml
from graph_builder import build_dependency_graph
from git_analyzer import get_commit_by_tag


def load_config(config_path):
    """Загрузка конфигурации из YAML файла."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден.")

    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def build_plantuml(graph):
    """Создание PlantUML графа."""
    lines = ["@startuml"]
    for commit, message, parents in graph:
        lines.append(f'"{commit[:7]}" : "{message}"')
        for parent in parents:
            lines.append(f'"{parent[:7]}" --> "{commit[:7]}"')
    lines.append("@enduml")
    return "\n".join(lines)


def main(config_path):
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        print(e)
        return

    repo_path = config.get("repository_path")
    if not os.path.exists(repo_path):
        print(f"Репозиторий по пути {repo_path} не найден.")
        return

    start_commit = get_commit_by_tag(repo_path, config["tag_name"])
    graph = build_dependency_graph(repo_path, start_commit)

    if not graph:
        print("Граф зависимостей пуст.")
        return

    plantuml_code = build_plantuml(graph)
    print("\n--- PlantUML Graph ---\n")
    print(plantuml_code)

    # Создаем директорию, если она не существует
    output_dir = './config'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Сохраняем граф в файл
    output_file = './config/output.puml'
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(plantuml_code)
        print(f"Граф зависимостей сохранен в {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении файла {output_file}: {e}")

    # Вызов PlantUML для визуализации
    try:
        plantuml_jar_path = 'config/plantuml.jar'  # Путь к вашему jar-файлу
        if os.path.exists(plantuml_jar_path):
            subprocess.run(['java', '-jar', plantuml_jar_path, output_file], check=True)
        else:
            print("Error: Unable to access jarfile config/plantuml.jar")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при вызове PlantUML: {e}")


if __name__ == "__main__":
    config_path = '../config/config.yaml'  # Путь к конфигурационному файлу
    main(config_path)
