# Практическое занятие №1. Введение, основы работы в командной строке

П.Н. Советов, РТУ МИРЭА

Научиться выполнять простые действия с файлами и каталогами в Linux из командной строки. Сравнить работу в командной строке Windows и Linux.

## Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

## Решение:
```
grep '^[^#]' /etc/passwd | grep -o '^[^:]*' | sort
```
## Результат:
![image](https://github.com/user-attachments/assets/129d3600-4499-407a-b773-3b488da5dff1)
## Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:

```
[root@localhost etc]# cat /etc/protocols ...
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```
## Решение:
```
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
## Результат:
![image](https://github.com/user-attachments/assets/759e8200-76d2-4961-8fb3-ec9b8609041b)
## Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```
Перед отправкой решения проверьте его в ShellCheck на предупреждения.

## Решение:
```
#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Usage: $0 \"Your message here\""
  exit 1
fi

# Сообщение
message="$1"

# Длина сообщения
length=${#message}

# Верхняя граница
echo "+$(printf '%0.s-' $(seq 1 $((length + 2))))+"

# Сообщение с границами
echo "| $message |"

# Нижняя граница
echo "+$(printf '%0.s-' $(seq 1 $((length + 2))))+"
```
## Результат:
![image](https://github.com/user-attachments/assets/478301b4-d2ab-4397-8ebb-7963e3f3908e)
## Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).

Пример для hello.c:

```
h hello include int main n printf return stdio void world
```

## Решение:
```
#!/bin/bash

file="$1"

identifiers=$(grep -o -E '\b[a-zA-Z]*\b' "$file" | sort -u)

echo "Идентификаторы:"
echo "$identifiers"
```
## Результат:
![image](https://github.com/user-attachments/assets/04ec63a0-1167-4dfd-8b18-61e610511882)
## Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

Например, пусть программа называется reg:

```
./reg banner
```

В результате для banner задаются правильные права доступа и сам banner копируется в /usr/local/bin.

## Решение:
```
#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Использование: $0 команда"
  exit 1
fi

# Имя команды
command=$1

# Проверка существования команды
if [ ! -f "$command" ]; then
  echo "Ошибка: команда $command не найдена."
  exit 1
fi

# Установка правильных прав доступа
chmod 755 "$command"

# Копирование команды в /usr/local/bin
sudo cp "$command" /usr/local/bin/

# Проверка успешности копирования
if [ $? -eq 0 ]; then
  echo "Команда $command успешно зарегистрирована в /usr/local/bin."
else
  echo "Ошибка: не удалось скопировать команду $command в /usr/local/bin."
fi
```
## Результат:
![image](https://github.com/user-attachments/assets/a3f404ae-c695-4170-b4ac-d64f3331c016)
## Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

## Решение:
```
#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Usage: $0 filename"
  exit 1
fi

# Имя файла
filename=$1

# Проверка расширения файла
extension="${filename##*.}"

# Функция для проверки комментария в первой строке
check_comment() {
  local file=$1
  local ext=$2
  local first_line=$(head -n 1 "$file")

  case "$ext" in
    c)
      if [[ "$first_line" =~ ^[[:space:]]*// ]]; then
        echo "Файл $file содержит комментарий в первой строке."
      else
        echo "Файл $file не содержит комментарий в первой строке."
      fi
      ;;
    js)
      if [[ "$first_line" =~ ^[[:space:]]*// ]]; then
        echo "Файл $file содержит комментарий в первой строке."
      else
        echo "Файл $file не содержит комментарий в первой строке."
      fi
      ;;
    py)
      if [[ "$first_line" =~ ^[[:space:]]*# ]]; then
        echo "Файл $file содержит комментарий в первой строке."
      else
        echo "Файл $file не содержит комментарий в первой строке."
      fi
      ;;
    *)
      echo "Неподдерживаемое расширение файла: $ext"
      ;;
  esac
}

# Проверка файла
check_comment "$filename" "$extension"
```
## Результат:
![image](https://github.com/user-attachments/assets/e6c9741a-bbcd-4a26-be44-6d8bb8d65d29)
![image](https://github.com/user-attachments/assets/37092817-de69-4955-a061-922d668b53ab)
## Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

## Решение:
```
#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Использование: $0 директория"
  exit 1
fi

# Заданный путь
directory=$1

# Проверка существования директории
if [ ! -d "$directory" ]; then
  echo "Ошибка: директория $directory не найдена."
  exit 1
fi

# Нахождение файлов-дубликатов
find "$directory" -type f -exec md5sum {} + | sort | uniq -w32 -dD | awk '{print $2}' | while read -r file; do
  echo "Найден дубликат: $file"
done
```
## Результат:
Создание файлов дубликтов: file1.txt; file2.txt; file3.txt и создание уникальных файлов: file4.txt; file5.txt

![image](https://github.com/user-attachments/assets/0b5ded06-5a30-4f80-9066-ae16391b73bd)
Поиск дубликатов:

![image](https://github.com/user-attachments/assets/92e3e5bf-5451-4264-b5d4-18ea2a0034c9)
## Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

## Решение:
```
#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Использование: $0 расширение"
  exit 1
fi

# Расширение файлов
extension=$1

# Имя архива
archive_name="archive_$extension.tar"

# Поиск и архивирование файлов
files=$(find . -type f -name "*.$extension")
if [ -n "$files" ]; then
  tar -cvf "$archive_name" $files
  
  # Проверка успешности архивирования
  if [ $? -eq 0 ]; then
    echo "Файлы с расширением .$extension успешно архивированы в $archive_name."
  else
    echo "Ошибка: не удалось создать архив $archive_name."
  fi
else
  echo "Файлы с расширением .$extension не найдены."
fi
```
## Результат:
![image](https://github.com/user-attachments/assets/8be0042b-e9df-4586-91fb-3d1423fceef9)
## Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

## Решение:
```
#!/bin/bash

# Проверка наличия двух аргументов
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file output_file"
    exit 1
fi

input_file="$1"
output_file="$2"

# Замена последовательностей из 4 пробелов на символ табуляции
sed 's/    /\t/g' "$input_file" > "$output_file"

echo "Замена завершена. Результат сохранен в $output_file"
```
## Результат:
![image](https://github.com/user-attachments/assets/757fc869-8812-441a-9709-fd19096c095d)
![image](https://github.com/user-attachments/assets/70e1873e-745a-4efa-90bd-94aa553f84e9)
![image](https://github.com/user-attachments/assets/f2195288-b2a3-40c3-85fc-4e7f6595231a)
## Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.

## Решение:
```

```
## Результат:

## Полезные ссылки

Линукс в браузере: https://bellard.org/jslinux/

ShellCheck: https://www.shellcheck.net/

Разработка CLI-приложений

Общие сведения

https://ru.wikipedia.org/wiki/Интерфейс_командной_строки
https://nullprogram.com/blog/2020/08/01/
https://habr.com/ru/post/150950/

Стандарты

https://www.gnu.org/prep/standards/standards.html#Command_002dLine-Interfaces
https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html

Реализация разбора опций

Питон

https://docs.python.org/3/library/argparse.html#module-argparse
https://click.palletsprojects.com/en/7.x/
