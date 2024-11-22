from git_analyzer import read_git_object, parse_commit_object


def build_dependency_graph(repo_path, start_commit):
    """Построение графа зависимостей."""
    queue = [start_commit]
    visited = {}
    graph = []

    while queue:
        commit = queue.pop(0)
        if commit in visited:
            continue
        visited[commit] = True
        print(f"Обрабатываем коммит: {commit}")
        try:
            data = read_git_object(repo_path, commit)
            parents, message = parse_commit_object(data)
            graph.append((commit, message, parents))
            queue.extend(parents)
        except FileNotFoundError:
            print(f"Ошибка: объект {commit} не найден в репозитории.")

    return graph
