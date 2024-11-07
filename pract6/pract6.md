# Юсубов Рашид Хазеинович ИКБО-63-23
# Практическое задание №6. Системы автоматизации сборки

П.Н. Советов, РТУ МИРЭА

Работа с утилитой Make.

Изучить основы языка утилиты make. Распаковать в созданный каталог [make.zip](make.zip), если у вас в в системе нет make.

Создать приведенный ниже Makefile и проверить его работоспособность.

```
dress: trousers shoes jacket
    @echo "All done. Let's go outside!"

jacket: pullover
    @echo "Putting on jacket."

pullover: shirt
    @echo "Putting on pullover."

shirt:
    @echo "Putting on shirt."

trousers: underpants
    @echo "Putting on trousers."

underpants:
    @echo "Putting on underpants."

shoes: socks
    @echo "Putting on shoes."

socks: pullover
    @echo "Putting on socks."
```

Визуализировать файл [civgraph.txt](civgraph.txt).

## Задача 1

Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: [civgraph.json](civgraph.json).

Пример:

```
> make mathematics
mining
bronze_working
sailing
astrology
celestial_navigation
pottery
writing
code_of_laws
foreign_trade
currency
irrigation
masonry
early_empire
mysticism
drama_poetry
mathematics
```

## Решение:

```Python
import json


def parse_civgraph(civgraph_file):
    # Чтение JSON-файла
    with open(civgraph_file, 'r') as file:
        data = json.load(file)

    return data


def generate_makefile(data, output_file):
    with open(output_file, 'w') as file:
        for target, dependencies in data.items():
            # Формируем правило для Makefile
            dep_str = " ".join(dependencies) if dependencies else ""
            file.write(f"{target}: {dep_str}\n")
            file.write(f"\t@echo {target}\n\n")  # Простое действие для примера


def main():
    civgraph_file = "civgraph.json"  # Имя файла с графом зависимостей
    output_file = "Makefile"  # Имя итогового Makefile

    # Чтение данных из civgraph.json
    data = parse_civgraph(civgraph_file)

    # Генерация Makefile
    generate_makefile(data, output_file)
    print(f"Makefile был сгенерирован в {output_file}")


if __name__ == "__main__":
    main()
```

## Результат:

![image](https://github.com/user-attachments/assets/2a874122-53ed-4e9c-9e93-bb94726032d8)

## Задача 2

Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".

## Решение:

```Python
import json


def load_dependencies(filename):
    """Загрузить граф зависимостей из файла JSON."""
    with open(filename, 'r') as file:
        return json.load(file)


def topological_sort(graph):
    """Проводим топологическую сортировку графа зависимостей."""
    visited = set()
    order = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        order.append(node)

    for node in graph:
        dfs(node)
    return order[::-1]


def create_makefile(dependencies):
    """Создаем Makefile с учетом топологического порядка зависимостей."""
    with open("Makefile", "w") as makefile:
        for target in dependencies:
            deps = ' '.join(dependencies[target])
            makefile.write(f"{target}: {deps}\n")
            makefile.write(f"\t@echo {target}\n\n")


def main():
    # Загрузить граф зависимостей
    graph = load_dependencies("civgraph.json")

    # Определить топологический порядок для Makefile
    sorted_technologies = topological_sort(graph)

    # Формируем словарь зависимостей для Makefile
    dependencies = {tech: graph.get(tech, []) for tech in sorted_technologies}

    # Создаем Makefile
    create_makefile(dependencies)
    print("Makefile создан.")


if __name__ == "__main__":
    main()
```

## Результат:




## Задача 3

Добавить цель clean, не забыв и про "животное".

## Решение:

```
```

## Результат:

## Задача 4

Написать makefile для следующего скрипта сборки:

```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```

Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data.
Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС.
В makefile должны быть, как минимум, следующие задачи: all, clean, archive.
Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.

## Решение:

```
```

## Результат:

## Полезные ссылки

Описание (рус.): https://unix1.jinr.ru/faq_guide/programming/make/make.html

Шпаргалка: https://devhints.io/makefile

Топологическая сортировка: https://ru.wikipedia.org/wiki/Топологическая_сортировка
