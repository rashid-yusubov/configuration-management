import yaml
import argparse


class ConfigLanguageConverter:
    def __init__(self):
        self.constants = {}

    def add_constant(self, value, name):
        """Добавление константы."""
        if not name.isidentifier():
            raise ValueError(f"Неверное имя константы: {name}")
        if not isinstance(value, (int, float, str, list, dict)):
            raise ValueError(f"Неверный тип значения константы: {type(value)}")
        self.constants[name] = value

    def convert_string(self, expr):
        """Преобразование выражений с константами."""
        if expr.startswith("#[") and expr.endswith("]"):
            constant_name = expr[2:-1]
            if constant_name in self.constants:
                return self.constants[constant_name]
            else:
                raise ValueError(f"Константа {constant_name} не найдена")
        return expr

    def to_config_language(self, data):
        """Конвертирует данные в формат учебного конфигурационного языка."""
        if isinstance(data, dict):
            return self._dict_to_config_language(data)
        elif isinstance(data, list):
            return self._list_to_config_language(data)
        elif isinstance(data, str):
            return self._string_to_config_language(self.convert_string(data))
        elif isinstance(data, (int, float)):
            return str(data)
        elif isinstance(data, bool):  # Исправление для булевых значений
            return "true" if data else "false"
        elif data is None:
            return "null"
        raise ValueError(f"Недопустимый тип данных: {type(data)}")

    def _dict_to_config_language(self, data):
        """Конвертирует словарь в формат конфигурационного языка."""
        result = "{\n"
        for key, value in data.items():
            key = key.replace("-", "_")  # Исправление для дефисов в ключах
            result += f"  {key} = {self.to_config_language(value)}\n"
        result += "}"
        return result

    def _list_to_config_language(self, data):
        """Конвертирует список в формат конфигурационного языка."""
        result = "'( "
        result += " ".join(self.to_config_language(item) for item in data)
        result += " )"
        return result

    def _string_to_config_language(self, data):
        """Конвертирует строку в формат конфигурационного языка."""
        return f'@"{data}"'


def read_input():
    """Считывает данные YAML из пользовательского ввода."""
    print("Введите YAML, завершите ввод пустой строкой или нажмите Ctrl+D для завершения:")
    yaml_input = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            yaml_input.append(line)
        except EOFError:
            break
    return "\n".join(yaml_input)


def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Преобразование YAML в учебный конфигурационный язык.")
    parser.add_argument("-f", "--file", help="Путь к YAML-файлу", type=str)
    return parser.parse_args()


def main():
    # Получение данных
    args = parse_args()
    if args.file:
        try:
            with open(args.file, "r") as file:
                yaml_input_str = file.read()
        except FileNotFoundError:
            print(f"Ошибка: файл {args.file} не найден.")
            return
    else:
        yaml_input_str = read_input()

    if not yaml_input_str.strip():
        print("Ошибка: Ввод пуст.")
        return

    # Разбор YAML
    try:
        data = yaml.safe_load(yaml_input_str)
    except yaml.YAMLError as e:
        print(f"Ошибка при разборе YAML: {e}")
        return

    # Обработка данных
    converter = ConfigLanguageConverter()

    # Пример добавления констант
    if "constants" in data:
        for name, value in data["constants"].items():
            try:
                converter.add_constant(value, name)
            except ValueError as e:
                print(f"Ошибка добавления константы: {e}")
                return

    # Преобразование и вывод
    try:
        print("\nПолученные данные:")
        print(converter.to_config_language(data))
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
