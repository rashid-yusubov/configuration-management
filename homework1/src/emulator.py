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
