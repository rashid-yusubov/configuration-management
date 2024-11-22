import os
import yaml
import subprocess
from git_analyzer import get_commit_by_tag
from graph_builder import build_dependency_graph, build_plantuml


def main(config_path):
    # Чтение конфигурации с указанием кодировки
    if not os.path.exists(config_path):
        print(f"Ошибка: файл конфигурации '{config_path}' не найден.")
        exit(1)

    with open(config_path, "r", encoding="utf-8") as file:  # Указание кодировки
        config = yaml.safe_load(file)

    repo_path = config["repository_path"]
    tag_name = config["tag_name"]
    output_file = config["output_file_path"]
    visualization_tool_path = config.get("visualization_tool_path")

    # Получение стартового коммита
    try:
        start_commit = get_commit_by_tag(repo_path, tag_name)
    except ValueError as e:
        print(e)
        return

    # Построение графа зависимостей
    graph = build_dependency_graph(repo_path, start_commit)
    if not graph:
        print("Граф зависимостей пуст.")
    else:
        print("Граф зависимостей построен успешно.")

    # Создание PlantUML
    plantuml_code = build_plantuml(graph)
    if not plantuml_code:
        print("Не удалось создать код для PlantUML.")
    else:
        print("\n--- PlantUML Graph ---\n")
        print(plantuml_code)  # Вывод в консоль

    # Сохранение результата
    try:
        with open(output_file, "w", encoding="utf-8") as file:  # Указание кодировки
            file.write(plantuml_code)
        print(f"Граф зависимостей успешно создан. Сохранён в {output_file}.")
    except Exception as e:
        print(f"Ошибка при сохранении файла {output_file}: {e}")

    # Если указан путь к инструменту визуализации, выполнить его
    if visualization_tool_path:
        try:
            subprocess.run(visualization_tool_path.split(), check=True)
            print(f"Граф визуализирован с использованием {visualization_tool_path}.")
        except Exception as e:
            print(f"Ошибка при вызове PlantUML: {e}")


if __name__ == "__main__":
    import sys

    # Путь по умолчанию для файла конфигурации
    default_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")

    # Использование пути по умолчанию, если не указан другой путь
    config_path = sys.argv[1] if len(sys.argv) > 1 else default_config_path

    main(config_path)
