import argparse
import json
import tarfile
import datetime
from pathlib import PurePosixPath


class ShellEmulator:
    """Эмулятор оболочки для управления виртуальной файловой системой."""
    def __init__(self, username, fs_path, log_path):
        self.username = username
        self.fs_path = fs_path
        self.log_path = log_path
        self.current_dir = '/'
        self.log_data = []
        self._file_system = {self.current_dir: []}  # инициализируем корневую директорию
        self.load_filesystem()

    def load_filesystem(self):
        """Загружает виртуальную файловую систему (архив tar)"""
        with tarfile.open(self.fs_path, mode="r") as tar:
            for member in tar.getmembers():
                member.name = "/" + member.name  # гарантируем, что путь начинается с /
                member_path = member.name.split("/")
                if len(member_path) == 2:
                    self._file_system["/"].append(member.name)
                    self._file_system[member.name] = []
                    continue

                parent = "/".join(member_path[:-1])
                if parent not in self._file_system:
                    self._file_system[parent] = []
                self._file_system[parent].append(member.name)
                self._file_system[member.name] = []

    def log_action(self, action):
        """Записывает действия в лог"""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": self.username,
            "action": action
        }
        self.log_data.append(entry)

    def _write_log(self):
        """Записывает накопленные логи в файл"""
        with open(self.log_path, "a") as log_file:
            for entry in self.log_data:
                json.dump(entry, log_file, indent=4)
                log_file.write("\n")

    def _get_absolute_path(self, path):
        """Преобразует путь в абсолютный относительно текущей директории"""
        if path in [".", "./"]:
            return self.current_dir
        elif path in ["..", "../"]:
            parent = "/".join(self.current_dir.strip("/").split("/")[:-1])
            return "/" + parent if parent else "/"
        elif path.startswith("/"):
            return "/" + path.strip("/")  # Убираем лишние слэши
        else:
            return str(PurePosixPath(self.current_dir) / path)

    def is_valid_file(self, path):
        """Проверяет, существует ли файл в виртуальной файловой системе"""
        return path in self._file_system and isinstance(self._file_system[path], list) and not self._file_system[path]

    def ls(self):
        """Выводит список файлов в текущей директории"""
        if self.current_dir not in self._file_system:
            print(f"Directory {self.current_dir} not found")
            self.log_action(f"ls failed for {self.current_dir}")
            return

        files = [filename.split("/")[-1] for filename in self._file_system[self.current_dir]]
        if files:
            print("\n".join(files))
        else:
            print("No files in directory.")
        self.log_action("ls")

    def cd(self, path):
        """Меняет текущую директорию"""
        absolute_path = self._get_absolute_path(path)
        if absolute_path in self._file_system:
            self.current_dir = absolute_path
            print(f"Changed directory to {self.current_dir}")
            self.log_action(f"cd {path}")
        else:
            print(f"Directory {path} not found")
            self.log_action(f"cd failed for {path}")

    def pwd(self):
        """Выводит текущую директорию"""
        print(f"Current directory: {self.current_dir}")
        self.log_action("pwd")

    def cp(self, source, destination):
        """Копирует файл из одного места в другое"""
        source_path = self._get_absolute_path(source)
        destination_path = self._get_absolute_path(destination)

        # Проверяем, существует ли исходный файл
        if not self.is_valid_file(source_path):
            print(f"Source file {source} does not exist.")
            self.log_action(f"cp failed for {source} to {destination}")
            return

        # Если destination — это директория
        if destination_path in self._file_system and isinstance(self._file_system[destination_path], list):
            destination_path = f"{destination_path.rstrip('/')}/{source_path.split('/')[-1]}"

        # Определяем родительскую директорию
        destination_dir = str(PurePosixPath(destination_path).parent)
        if destination_dir not in self._file_system:
            print(f"Destination directory {destination_dir} does not exist.")
            self.log_action(f"cp failed for {source} to {destination}")
            return

        # Убедимся, что директория существует
        if destination_dir not in self._file_system:
            self._file_system[destination_dir] = []

        # Копируем файл
        self._file_system[destination_path] = self._file_system[source_path]
        if destination_path not in self._file_system[destination_dir]:
            self._file_system[destination_dir].append(destination_path)

        print(f"Copied {source} to {destination}")
        self.log_action(f"cp {source} {destination}")

    def whoami(self):
        """Выводит имя пользователя"""
        print(f"User: {self.username}")
        self.log_action("whoami")

    def exit(self):
        """Завершает работу эмулятора и записывает логи"""
        self.log_action("exit")
        self._write_log()
        exit(0)

    def run(self):
        """Основной цикл работы эмулятора"""
        while True:
            command = input(f"{self.username}@emulator:~{self.current_dir}$ ").strip().split()
            if not command:
                continue
            if command[0] == "ls":
                self.ls()
            elif command[0] == "cd":
                if len(command) > 1:
                    self.cd(command[1])
                else:
                    print("Необходимо указать путь для команды 'cd'.")
            elif command[0] == "pwd":
                self.pwd()
            elif command[0] == "cp":
                if len(command) > 2:
                    self.cp(command[1], command[2])
                else:
                    print("Необходимо указать исходный и конечный путь для команды 'cp'.")
            elif command[0] == "whoami":
                self.whoami()
            elif command[0] == "exit":
                self.exit()
            else:
                print("Неизвестная команда")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument("--username", required=True, help="Имя пользователя для оболочки")
    parser.add_argument("--fs", required=True, help="Путь к виртуальной файловой системе (файл tar)")
    parser.add_argument("--log", required=True, help="Путь к файлу лога")
    args = parser.parse_args()

    emulator = ShellEmulator(args.username, args.fs, args.log)
    emulator.run()