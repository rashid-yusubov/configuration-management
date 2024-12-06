#  Инструмент командной строки для учебного конфигурационного языка

## 1. Описание
Этот проект выполняет преобразование входного файла в формате YAML в текст на учебном конфигурационном языке.

### Структура проекта:

```css
homework3/
├── src/
│   └── main.py          # Основной файл для запуска программы
├── config/
│   └── config.yaml      # Конфигурационный файл
└── README.md            # Документация
```

## 2. Функции и настройки

## 3. Команды для сборки и запуска проекта

### Создание виртуального окружения

   ```python
   python -m venv .venv
   ```

### Активация виртуального окружения (Windows)

   ```bash
   .venv\Scripts\activate
   ```

### Активация виртуального окружения (MacOS/Linux)

   ```bash
   source venv/bin/activate
   ```

### Установка необходимых библиотек:

   ```bash
   pip install -r requirements.txt
   ```

### Запуск проекта

   ```bash
   cd src
   python main.py
   ```

## 4. Примеры использования

### 1. Веб-приложение (Web Application Configuration)

#### YAML:

```yaml
app:
  name: WebApp
  version: 2.1
  settings:
    theme: "light"
    max_sessions: 200
    enable_notifications: true
  features:
    - "UserManagement"
    - "Analytics"
    - "IntegrationAPI"
constants:
  max_connections: 500
server:
  host: "192.168.1.10"
  port: 8080
  max_clients: #[max_connections]
```

#### Учебный конфигурационный язык:

```Bash
{
  app = {
    name = @"WebApp"
    version = 2.1
    settings = {
      theme = @"light"
      max_sessions = 200
      enable_notifications = true
    }
    features = '( @"UserManagement" @"Analytics" @"IntegrationAPI" )
  }
  constants = {
    max_connections = 500
  }
  server = {
    host = @"192.168.1.10"
    port = 8080
    max_clients = 500
  }
}
```

### 2. Настройки датчика IoT (IoT Sensor Configuration)

#### YAML:

```yaml
sensor:
  id: "sensor-001"
  location: "Building-5"
  parameters:
    threshold: 75
    interval: 15
  alerts:
    email: "alerts@domain.com"
    sms: "+1234567890"
constants:
  default_interval: 10
device:
  type: "Temperature"
  firmware_version: 1.3
  interval: #[default_interval]
```

#### Учебный конфигурационный язык:

```Bash
{
  sensor = {
    id = @"sensor-001"
    location = @"Building-5"
    parameters = {
      threshold = 75
      interval = 15
    }
    alerts = {
      email = @"alerts@domain.com"
      sms = @"1234567890"
    }
  }
  constants = {
    default_interval = 10
  }
  device = {
    type = @"Temperature"
    firmware_version = 1.3
    interval = 10
  }
}
```

### 3. Конфигурация игры (Game Settings)

#### YAML:

```yaml
game:
  title: "Space Adventure"
  version: 3.5
  settings:
    difficulty: "Hard"
    max_players: 4
    enable_cheats: false
  assets:
    textures:
      resolution: "4K"
      quality: "High"
    sounds:
      music_volume: 70
      effects_volume: 85
constants:
  default_players: 1
gameplay:
  mode: "Multiplayer"
  default_players: #[default_players]
```

#### Учебный конфигурационный язык:

```Bash
{
  game = {
    title = @"Space Adventure"
    version = 3.5
    settings = {
      difficulty = @"Hard"
      max_players = 4
      enable_cheats = false
    }
    assets = {
      textures = {
        resolution = @"4K"
        quality = @"High"
      }
      sounds = {
        music_volume = 70
        effects_volume = 85
      }
    }
  }
  constants = {
    default_players = 1
  }
  gameplay = {
    mode = @"Multiplayer"
    default_players = 1
  }
}
```

## 5. Результаты прогона тестов:

![image](https://github.com/user-attachments/assets/f8d3e69b-4572-45d7-bab0-5d0a2a1ea3eb)
