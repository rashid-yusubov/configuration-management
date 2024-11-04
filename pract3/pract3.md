# Юсубов Рашид Хазеинович ИКБО-63-23
# Практическое занятие №3. Конфигурационные языки

П.Н. Советов, РТУ МИРЭА

Разобраться, что собой представляют программируемые конфигурационные языки (Jsonnet, Dhall, CUE).

## Задача 1

Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

## Решение:
```Jsonnet
{
  groups: ["ИКБО-1-20", "ИКБО-2-20", "ИКБО-3-20", "ИКБО-4-20", "ИКБО-5-20", 
           "ИКБО-6-20", "ИКБО-7-20", "ИКБО-8-20", "ИКБО-9-20", "ИКБО-10-20", 
           "ИКБО-11-20", "ИКБО-12-20", "ИКБО-13-20", "ИКБО-14-20", "ИКБО-15-20",
           "ИКБО-16-20", "ИКБО-17-20", "ИКБО-18-20", "ИКБО-19-20", "ИКБО-20-20", 
           "ИКБО-21-20", "ИКБО-22-20", "ИКБО-23-20", "ИКБО-24-20", "ИКБО-63-23"],

  students: [
    { name: "Иванов И.И.", age: 19, group: "ИКБО-4-20" },
    { name: "Петров П.П.", age: 20, group: "ИКБО-5-20" },
    { name: "Сидоров С.С.", age: 18, group: "ИКБО-6-20" },
    { name: "Юсубов Р.Х.", age: 20, group: "ИКБО-63-23" },
  ]
}
```

## Результат:

![image](https://github.com/user-attachments/assets/dfba45f5-ef35-4091-9e3c-109ef22e6bc2)


## Задача 2

Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

```JSON
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    <добавьте ваши данные в качестве четвертого студента>
  ],
  "subject": "Конфигурационное управление"
} 
```

Для решения дальнейших задач потребуется программа на Питоне, представленная ниже. Разбираться в самом языке Питон при этом необязательно.

```Python
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = a
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))

```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF:

## Решение:

```
-- Файл: students.dhall

let Group = List Text
let Student = { age : Natural, group : Text, name : Text }

let studentsData = 
      { groups = [ "ИКБО-1-20", "ИКБО-2-20", "ИКБО-3-20", "ИКБО-4-20", "ИКБО-5-20",
                   "ИКБО-6-20", "ИКБО-7-20", "ИКБО-8-20", "ИКБО-9-20", "ИКБО-10-20",
                   "ИКБО-11-20", "ИКБО-12-20", "ИКБО-13-20", "ИКБО-14-20", "ИКБО-15-20",
                   "ИКБО-16-20", "ИКБО-17-20", "ИКБО-18-20", "ИКБО-19-20", "ИКБО-20-20",
                   "ИКБО-21-20", "ИКБО-22-20", "ИКБО-23-20", "ИКБО-24-20", "ИКБО-63-23" ] : Group,
      
        students = 
            [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
            , { age = 20, group = "ИКБО-5-20", name = "Петров П.П." }
            , { age = 18, group = "ИКБО-6-20", name = "Сидоров С.С." }
            , { age = 18, group = "ИКБО-6-20", name = "Юсубов Р.Х." }
            ] : List Student
      }

in studentsData
```

## Результат:

```
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20",
    "ИКБО-63-23"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 20,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-6-20",
      "name": "Сидоров С.С."
    },
    {
      "age": 18,
      "group": "ИКБО-6-20",
      "name": "Юсубов Р.Х."
    }
  ]
}
```

## Задача 3

Язык нулей и единиц.

```
10
100
11
101101
000
```

## Решение:

```
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = 10 | 100 | 11 | 101101 | 000
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

## Результат:

![image](https://github.com/user-attachments/assets/7a20573f-e193-4c14-a8fe-4b919c55a2b8)

## Задача 4

Язык правильно расставленных скобок двух видов.

```
(({((()))}))
{}
{()}
()
{}
```

## Решение:
```
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = ( E ) | { E } |
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))

```
## Результат:

![image](https://github.com/user-attachments/assets/452b880c-2e84-47ad-91ef-f8ee78cb7cba)


## Задача 5

Язык выражений алгебры логики.

```
((~(y & x)) | (y) & ~x | ~x) & x
y & ~(y)
(~(y) & y & ~y)
~x
~((x) & y | (y) | (x)) & x | x | (y & ~y)
```

## Решение:
```
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = "~" E | E "&" E | E "|" E | "(" E ")" | "x" | "y"
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))

```

## Полезные ссылки

Configuration complexity clock: https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html

Json: http://www.json.org/json-ru.html

Язык Jsonnet: https://jsonnet.org/learning/tutorial.html

Язык Dhall: https://dhall-lang.org/

Учебник в котором темы построения синтаксических анализаторов (БНФ, Lex/Yacc) изложены подробно: https://ita.sibsutis.ru/sites/csc.sibsutis.ru/files/courses/trans/LanguagesAndTranslationMethods.pdf

Полезные материалы для разработчика (очень рекомендую посмотреть слайды и прочие ссылки, все это актуально и для других тем нашего курса): https://habr.com/ru/company/JetBrains-education/blog/547768/
