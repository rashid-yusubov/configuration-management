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
        data = read_git_object(repo_path, commit)
        parents, message = parse_commit_object(data)
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
