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