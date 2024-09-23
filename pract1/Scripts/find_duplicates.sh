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
