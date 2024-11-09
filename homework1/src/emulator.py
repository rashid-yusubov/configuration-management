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
