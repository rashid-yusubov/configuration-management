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
from collections import defaultdict, deque


def load_dependencies(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def build_graph(dependencies):
    graph = defaultdict(list)
    # Сначала добавляем все узлы в граф и их зависимости
    for item, deps in dependencies.items():
        graph[item]  # Гарантируем, что каждый элемент есть в графе
        for dep in deps:
            graph[dep]  # Также добавляем зависимость как узел
            graph[dep].append(item)
    return graph


def topological_sort(graph):
    in_degree = {node: 0 for node in graph}  # Инициализируем in_degree для всех узлов
    for deps in graph.values():
        for dep in deps:
            in_degree[dep] += 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    sorted_items = []

    while queue:
        node = queue.popleft()
        sorted_items.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_items


def main(target):
    dependencies = load_dependencies('civgraph.json')
    graph = build_graph(dependencies)

    # Добавляем цель как узел, если у нее есть зависимости
    if target in dependencies:
        graph[target]  # Убедимся, что цель есть в графе

    sorted_items = topological_sort(graph)

    # Находим индекс цели и выводим все элементы перед ней
    if target in sorted_items:
        index = sorted_items.index(target)
        for item in sorted_items[:index + 1]:
            print(item)


if __name__ == "__main__":
    target = "mathematics"  # Здесь можно указать любую цель
    main(target)
```

## Результат:

![image](https://github.com/user-attachments/assets/87d7e59f-4a97-4ed9-89e0-6e9366b3d289)

## Задача 2

Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".

## Решение:

```
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
