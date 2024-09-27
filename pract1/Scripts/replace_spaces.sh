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
