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
