import unittest
from homework3.src.main import ConfigLanguageConverter


class TestConfigLanguageConverter(unittest.TestCase):
    def setUp(self):
        self.converter = ConfigLanguageConverter()
        self.converter.add_constant(100, "max_connections")  # Пример константы

    def test_single_line_comment(self):
        """Тест однострочного комментария."""
        self.assertEqual(self.converter.to_config_language({"comment": "% This is a comment"}),
                         '{\n  comment = @"% This is a comment"\n}')

    def test_multiline_comment(self):
        """Тест многострочного комментария."""
        comment = "(*\nThis is a\nmultiline comment\n*)"
        self.assertEqual(self.converter.to_config_language({"comment": comment}),
                         '{\n  comment = @"(*\nThis is a\nmultiline comment\n*)"\n}')

    def test_array(self):
        """Тест массивов."""
        data = ["value1", "value2", "value3"]
        self.assertEqual(self.converter.to_config_language(data), "'( @\"value1\" @\"value2\" @\"value3\" )")

    def test_dict(self):
        """Тест словаря."""
        data = {"key1": "value1", "key2": "value2"}
        self.assertEqual(self.converter.to_config_language(data),
                         '{\n  key1 = @"value1"\n  key2 = @"value2"\n}')

    def test_numbers(self):
        """Тест чисел."""
        self.assertEqual(self.converter.to_config_language(42), "42")
        self.assertEqual(self.converter.to_config_language(3.14), "3.14")

    def test_strings(self):
        """Тест строк."""
        self.assertEqual(self.converter.to_config_language("This is a string"), '@"This is a string"')

    def test_constants_declaration(self):
        """Тест объявления констант."""
        self.converter.add_constant(50, "max_users")
        self.assertEqual(self.converter.constants["max_users"], 50)

    def test_constants_usage(self):
        """Тест вычисления констант."""
        expression = "#[max_connections]"
        self.assertEqual(self.converter.convert_string(expression), "100")

    def test_nested_structures(self):
        """Тест вложенных структур."""
        data = {
            "app": {
                "name": "MyApp",
                "version": 1.0,
                "features": ["Auth", "Logging"]
            },
            "server": {
                "host": "localhost",
                "port": 8080
            }
        }
        expected_output = """{
  app = {
  name = @"MyApp"
  version = 1.0
  features = '( @"Auth" @"Logging" )
}
  server = {
  host = @"localhost"
  port = 8080
}
}"""
        self.assertEqual(self.converter.to_config_language(data), expected_output)

    def test_empty_input(self):
        """Тест обработки пустого ввода."""
        self.assertEqual(self.converter.to_config_language({}), "{\n}")

    def test_invalid_constant(self):
        """Тест обращения к несуществующей константе."""
        with self.assertRaises(ValueError):
            self.converter.convert_string("#[undefined_constant]")


if __name__ == "__main__":
    unittest.main()
