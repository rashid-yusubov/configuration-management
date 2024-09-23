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