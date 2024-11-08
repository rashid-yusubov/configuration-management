import os
import tarfile
import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from subprocess import run


# Класс эмулятора оболочки
class ShellEmulator:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.tar_file = self.config['filesystem']
        self.current_directory = '/'
        self.initialize_virtual_filesystem()
        self.command_history = []

    def load_config(self, config_file):
        """Загружаем конфигурацию из JSON"""
        with open(config_file, 'r') as f:
            return json.load(f)

    def initialize_virtual_filesystem(self):
        """Инициализация виртуальной файловой системы из tar"""
        self.fs = tarfile.open(self.tar_file, 'r')

    def execute_command(self, command):
        """Исполнение команд оболочки"""
        if command.startswith('ls'):
            return self.ls()
        elif command.startswith('cd'):
            return self.cd(command)
        elif command.startswith('pwd'):
            return self.pwd()
        elif command.startswith('du'):
            return self.du(command)
        elif command.startswith('uniq'):
            return self.uniq(command)
        elif command == 'exit':
            self.exit_shell()
        elif command == 'help':
            return self.help()
        else:
            return f"Command not found: {command}"

    def ls(self):
        """Команда ls - вывод списка файлов"""
        files = [member.name for member in self.fs.getmembers() if member.isdir()]
        return "\n".join(files)

    def cd(self, command):
        """Команда cd - изменение текущей директории"""
        path = command.split(' ')[1] if len(command.split(' ')) > 1 else ''
        if self.fs.getmember(path).isdir():
            self.current_directory = path
            return f"Changed directory to {self.current_directory}"
        else:
            return f"cd: no such directory: {path}"

    def pwd(self):
        """Команда pwd - вывод текущего пути"""
        return self.current_directory

    def du(self, command):
        """Команда du - вывод размера файлов и каталогов"""
        path = command.split(' ')[1] if len(command.split(' ')) > 1 else self.current_directory
        total_size = sum(member.size for member in self.fs.getmembers() if member.name.startswith(path))
        return f"Total size of {path}: {total_size} bytes"

    def uniq(self, command):
        """Команда uniq - фильтрация дубликатов"""
        file_path = command.split(' ')[1] if len(command.split(' ')) > 1 else ''
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            unique_lines = list(set(lines))
            return ''.join(unique_lines)
        except Exception as e:
            return f"Error: {e}"

    def exit_shell(self):
        """Команда exit - завершение эмулятора"""
        self.fs.close()
        exit(0)

    def help(self):
        """Команда help - выводит доступные команды"""
        help_text = """
        Available commands:
        ls       - List files and directories
        cd <dir> - Change current directory
        pwd      - Print the current working directory
        du <dir> - Display disk usage for a directory
        uniq <file> - Remove duplicate lines from a file
        exit     - Exit the emulator
        help     - Display this help message
        """
        return help_text

    def log_action(self, action):
        """Запись действия в лог-файл CSV"""
        with open(self.config['log_file'], 'a', newline='') as log:
            writer = csv.writer(log)
            writer.writerow([action])


# Класс GUI
class ShellGUI(tk.Tk):
    def __init__(self, emulator):
        super().__init__()
        self.emulator = emulator
        self.title("Shell Emulator")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.output_text = tk.Text(self, height=15, width=70)
        self.output_text.pack()

        self.command_entry = tk.Entry(self, width=70)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.pack()

    def execute_command(self, event):
        """Обработка ввода команды"""
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)

        result = self.emulator.execute_command(command)
        self.emulator.log_action(command)  # Логируем команду
        self.output_text.insert(tk.END, f"$ {command}\n{result}\n\n")
        self.output_text.yview(tk.END)  # Прокручиваем до конца
