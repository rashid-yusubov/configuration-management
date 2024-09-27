#!/bin/bash

# Проверка наличия одного аргумента
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

directory="$1"

# Поиск и вывод названий всех пустых текстовых файлов
find "$directory" -type f -name "*.txt" -empty
