import yaml


class ConfigLanguageConverter:
    def __init__(self):
        self.constants = {}

    def add_constant(self, value, name):
        """Добавление константы."""
        if not name.isidentifier():
            raise ValueError(f"Неверное имя константы: {name}")
        self.constants[name] = value

    def convert_string(self, expr):
        """Преобразование выражений с константами."""
        if expr.startswith("#[") and expr.endswith("]"):
            constant_name = expr[2:-1]
            if constant_name in self.constants:
                return str(self.constants[constant_name])
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
            return self._string_to_config_language(data)
        elif isinstance(data, (int, float)):
            return str(data)
        return str(data)

    def _dict_to_config_language(self, data):
        """Конвертирует словарь в формат конфигурационного языка."""
        result = "{\n"
        for key, value in data.items():
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


def main():
    # Считывание YAML с входа
    print("Введите YAML:")
    try:
        yaml_input = input()
        data = yaml.safe_load(yaml_input)
    except yaml.YAMLError as e:
        print(f"Ошибка при разборе YAML: {e}")
        return

    # Обработка данных
    converter = ConfigLanguageConverter()

    # Пример добавления констант
    if "constants" in data:
        for name, value in data["constants"].items():
            converter.add_constant(value, name)

    # Преобразование и вывод
    try:
        print("\nПолученные данные:")
        print(converter.to_config_language(data))
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
