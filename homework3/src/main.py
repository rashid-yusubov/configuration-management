import yaml
import sys
import re


class ConfigLanguageConverter:
    def __init__(self):
        self.constants = {}

    def parse_yaml(self, yaml_input):
        try:
            return yaml.safe_load(yaml_input)
        except yaml.YAMLError as e:
            raise ValueError(f"Ошибка парсинга YAML: {e}")

    def to_config_language(self, data):
        if isinstance(data, dict):
            return self.convert_dict(data)
        elif isinstance(data, list):
            return self.convert_list(data)
        elif isinstance(data, str):
            return f'@"{data}"'
        elif isinstance(data, (int, float)):
            return str(data)
        else:
            raise ValueError(f"Недопустимый тип данных: {type(data)}")

    def convert_dict(self, data):
        result = ["{"]
        for key, value in data.items():
            if not re.match(r'^[_a-zA-Z]+$', key):
                raise ValueError(f"Недопустимое имя: {key}")
            value_repr = self.to_config_language(value)
            result.append(f" {key} = {value_repr}")
        result.append("}")
        return "\n".join(result)

    def convert_list(self, data):
        values = " ".join(self.to_config_language(value) for value in data)
        return f"'( {values} )"

    def define_constant(self, name, value):
        if not re.match(r'^[_a-zA-Z]+$', name):
            raise ValueError(f"Недопустимое имя для константы: {name}")
        self.constants[name] = value

    def evaluate_constant(self, name):
        if name not in self.constants:
            raise ValueError(f"Неопределенная константа: {name}")
        return self.constants[name]


def main():
    input_data = sys.stdin.read()
    converter = ConfigLanguageConverter()

    try:
        yaml_data = converter.parse_yaml(input_data)
        output = converter.to_config_language(yaml_data)
        print(output)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
