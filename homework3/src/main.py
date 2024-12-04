import yaml
import sys
import re


class ConfigLanguageConverter:
    def __init__(self):
        self.constants = {}
        self.indent = 2  # Уровень отступа

    def parse_yaml(self, yaml_input):
        """
        Парсинг YAML.
        """
        try:
            return yaml.safe_load(yaml_input)
        except yaml.YAMLError as e:
            raise ValueError(f"Ошибка парсинга YAML: {e}")

    def to_config_language(self, data, level=0):
        """
        Преобразует данные в конфигурационный язык с отступами.
        """
        if isinstance(data, dict):
            return self.convert_dict(data, level)
        elif isinstance(data, list):
            return self.convert_list(data, level)
        elif isinstance(data, str):
            return self.convert_string(data)
        elif isinstance(data, (int, float)):
            return str(data)
        else:
            raise ValueError(f"Недопустимый тип данных: {type(data)}")

    def convert_dict(self, data, level):
        """
        Преобразует словарь в формат { key = value } с отступами.
        """
        indent = ' ' * (level * self.indent)
        result = ["{"]
        for key, value in data.items():
            value_repr = self.to_config_language(value, level + 1)
            result.append(f"{indent}{' ' * self.indent}{key} = {value_repr}")
        result.append(f"{indent}}}")
        return "\n".join(result)

    def convert_list(self, data, level):
        """
        Преобразует массив в формат '( value value ... )' с отступами.
        """
        values = " ".join(self.to_config_language(value, level + 1) for value in data)
        return f"'( {values} )"

    def convert_string(self, value):
        """
        Обрабатывает строки, включая вычисление констант.
        """
        if value.startswith('#[') and value.endswith(']'):
            constant_name = value[2:-1]
            if constant_name in self.constants:
                return self.constants[constant_name]
            else:
                raise ValueError(f"Неизвестная константа: {constant_name}")
        return f'@"{value}"'

    def add_constant(self, value, name):
        """
        Добавляет константу в таблицу.
        """
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name):
            raise ValueError(f"Недопустимое имя для константы: {name}")
        self.constants[name] = self.to_config_language(value)


def main():
    """
    Основной метод для запуска.
    """
    print("Введите YAML:")
    input_data = sys.stdin.read().strip()
    if not input_data:
        print("Ошибка: Входные данные отсутствуют. Укажите YAML-файл или передайте данные через stdin.", file=sys.stderr)
        return

    print("Полученные данные для обработки:")
    print(input_data)

    converter = ConfigLanguageConverter()

    try:
        yaml_data = converter.parse_yaml(input_data)

        # Пример обработки констант, если они указаны в YAML.
        if 'constants' in yaml_data:
            for name, value in yaml_data['constants'].items():
                converter.add_constant(value, name)

        output = converter.to_config_language(yaml_data)
        print("Результат преобразования:")
        print(output)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
