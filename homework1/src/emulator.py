import argparse
import json
import tarfile
import datetime
from pathlib import PurePosixPath

class ShellEmulator:
    def __init__(self, username, fs_path, log_path):
        self.username = username
        self.fs_path = fs_path
        self.log_path = log_path
        self.current_dir = '/'
        self.log_data = []
        self._file_system = {self.current_dir: []}  # Инициализация корневой директории

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

