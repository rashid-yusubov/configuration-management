from git_analyzer import read_git_object  # Добавляем импорт


def build_dependency_graph(repo_path, start_commit):
    """Построение графа зависимостей."""
    queue = [start_commit]
    visited = {}
    graph = []

    print(f"Начало построения графа для коммита {start_commit}")

    while queue:
        commit = queue.pop(0)
        print(f"Обрабатываем коммит: {commit}")  # Логирование обработки коммита
        if commit in visited:
            continue
        visited[commit] = True

        try:
            data = read_git_object(repo_path, commit)
        except FileNotFoundError:
            print(f"Ошибка при чтении объекта {commit}: Объект не найден в репозитории.")
            continue  # Пропускаем этот коммит, если он не найден

        parents, message = parse_commit_object(data)
        print(f"Сообщение коммита: {message}")  # Логируем сообщение коммита
        graph.append((commit, message, parents))
        queue.extend(parents)

    return graph


def build_plantuml(graph):
    """Создание PlantUML графа."""
    lines = ["@startuml"]
    for commit, message, parents in graph:
        lines.append(f'"{commit[:7]}" : "{message}"')
        for parent in parents:
            lines.append(f'"{parent[:7]}" --> "{commit[:7]}"')
    lines.append("@enduml")
    return "\n".join(lines)
