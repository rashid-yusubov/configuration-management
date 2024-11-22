import yaml
from git_analyzer import get_commit_data
from graph_builder import build_plantuml_graph

def main():
    # Чтение конфигурации
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    repo_path = config['repository_path']
    tag_name = config['tag_name']

    # Получаем данные о коммитах
    commits = get_commit_data(repo_path, tag_name)

    # Строим граф зависимостей
    plantuml_code = build_plantuml_graph(commits)

    # Сохраняем результат в файл
    with open(config['output_file_path'], 'w') as f:
        f.write(plantuml_code)

    print("Graph generated and saved to:", config['output_file_path'])

if __name__ == '__main__':
    main()
