# Эмулятор для оболочки языка OS

## 1. Общее описание

Этот проект представляет собой эмулятор оболочки языка OS, реализованный на Python. Эмулятор поддерживает базовые команды командной строки, такие как `ls`, `cd`, `pwd`, `cp`, `whoami` и `exit`. Все действия пользователя логируются в формате JSON с временными метками, а виртуальная файловая система загружается из архива tar.

### Основные особенности:
- Эмуляция команд UNIX-подобной оболочки.
- Поддержка виртуальной файловой системы, загружаемой из архива tar.
- Логирование всех действий пользователя.
- Поддержка базовых команд для работы с файлами и директориями.

### Структура проекта:
```css
homework1/
├── config/
│   ├── session_log.json  # Файл для логов
│   └── virtual_fs.tar # Виртуальная файловая система
├── src/
│   └── shell_emulator.py # Основной файл с программой
└── tests/
    └── test_shell_emulator.py # Файл с тестами
```
## 2. Описание всех функций и настроек

### Класс `ShellEmulator`

#### `__init__(self, username, fs_path, log_path)`

```Python
 def __init__(self, username, fs_path, log_path):
    self.username = username
    self.fs_path = fs_path
    self.log_path = log_path
    self.current_dir = '/'
    self.log_data = []
    self._file_system = {self.current_dir: []}  # инициализируем корневую директорию
    self.load_filesystem()
```

- **Описание**: Инициализирует эмулятор оболочки.
- **Параметры**:
  - `username`: Имя пользователя для эмулятора.
  - `fs_path`: Путь к архиву tar с виртуальной файловой системой.
  - `log_path`: Путь к файлу для записи логов.

#### `load_filesystem(self)`

```Python
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
```

- **Описание**: Загружает виртуальную файловую систему из архива tar.

#### `log_action(self, action)`

```Python
def log_action(self, action):
    """Записывает действия в лог"""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": self.username,
        "action": action
    }
    self.log_data.append(entry)
```

- **Описание**: Записывает действия в лог.

#### `ls(self)`

```Python
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
```

- **Описание**: Выводит список файлов в текущей директории.

#### `cd(self, path)`

```Python
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
```

- **Описание**: Меняет текущую директорию.
- **Параметры**:
  - `path`: Путь к новой директории.

#### `pwd(self)`

```Python
def pwd(self):
    """Выводит текущую директорию"""
    print(f"Current directory: {self.current_dir}")
    self.log_action("pwd")
```

- **Описание**: Выводит текущую директорию.

#### `cp(self, source, destination)`

```Python
def cp(self, source, destination):
    """Копирует файл из одного места в другое"""
    source_path = self._get_absolute_path(source)
    destination_path = self._get_absolute_path(destination)

    if not self.is_valid_file(source_path):
        print(f"Source file {source} does not exist.")
        self.log_action(f"cp failed for {source} to {destination}")
        return

    destination_dir = str(PurePosixPath(destination_path).parent)
    if destination_dir not in self._file_system:
        print(f"Destination directory {destination} does not exist.")
        self.log_action(f"cp failed for {source} to {destination}")
        return

    # Добавляем файл в виртуальную файловую систему
    self._file_system[destination_path] = []
    self._file_system[destination_dir].append(destination_path)
    print(f"Copied {source} to {destination}")
    self.log_action(f"cp {source} {destination}")
```

- **Описание**: Копирует файл из исходной директории в конечную.
- **Параметры**:
  - `source`: Путь к исходному файлу.
  - `destination`: Путь к конечному файлу.

#### `whoami(self)`

```Python
def whoami(self):
    """Выводит имя пользователя"""
    print(f"User: {self.username}")
    self.log_action("whoami")
```

- **Описание**: Выводит имя текущего пользователя.

#### `exit(self)`

```Python
def exit(self):
    """Завершает работу эмулятора и записывает логи"""
    print("Выход из эмулятора оболочки.")
    self.log_action("exit")
    self._write_log()
    exit(0)
```

- **Описание**: Завершает работу эмулятора и записывает логи.

#### `run(self)`

```Python
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
```

- **Описание**: Основной цикл работы эмулятора, ожидающий ввода команд от пользователя.

## 3. Описание команд для сборки проекта

Для работы с проектом необходимо иметь установленный Python 3.12

### Клонирование репозитория:

```bash
git clone https://github.com/Rashid-Yusubov/Configuration-management.git
cd Configuration-management
```

### Установка зависимостей:

```bash
cd homework1
pip install -r requirements.txt
```

### Запуск эмулятора:
```bash
python "src/shell_emulator.py" --username "username" --fs "config/virtual_fs.tar" --log "config/session_log.json"
```
## 4. Пример использования:

![prewiew (1) (1)](https://github.com/user-attachments/assets/bd67fff9-6052-48f1-9745-7adc7fd82fe6)

## 5. Результаты прогона тестов:

![image](https://github.com/user-attachments/assets/749945c3-f281-4827-b8a1-7adbd60ff6ff)
