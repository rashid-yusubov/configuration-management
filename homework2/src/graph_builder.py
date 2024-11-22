def build_plantuml_graph(commits):
    """
    Строит граф зависимостей для коммитов в формате PlantUML.
    Возвращает строку с кодом PlantUML.
    """
    plantuml_code = "@startuml\n"
    for commit in commits:
        plantuml_code += f'  "{commit["sha1"]}" : "{commit["message"]}"\n'
        # Добавляем связи с родительскими коммитами
        # Предположим, что родительский коммит передается в list
        for parent_sha1 in commit.get("parents", []):
            plantuml_code += f'  "{commit["sha1"]}" --> "{parent_sha1}"\n'
    plantuml_code += "@enduml\n"
    return plantuml_code
