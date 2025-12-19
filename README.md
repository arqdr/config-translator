# Конфигурационный транслятор

## Общее описание
Инструмент командной строки на Python для преобразования текста из учебного конфигурационного языка в TOML формат. Использует библиотеку Lark для парсинга. Поддерживает словари, константы, строки, числа и константные вычисления в постфиксной форме.

## Описание всех функций и настроек
### Синтаксис входного языка:
- Однострочные комментарии: `% Это комментарий`
- Числа: `[+-]?\d+`
- Словари: `@{ имя = значение; ... }`
- Имена: `[_a-z]+`
- Значения: числа, строки, словари
- Строки: `[[Это строка]]`
- Константы: `имя = значение`
- Константные выражения: `$имя 1 +$` (постфиксная форма)

### Поддерживаемые операции:
1. `+` - сложение
2. `-` - вычитание  
3. `*` - умножение
4. `/` - целочисленное деление
5. `mod` - остаток от деления (функция)

### Ключи командной строки:
```bash
usage: python src/cli.py [-h] -o OUTPUT

Конвертер конфигурационного языка в TOML

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Путь к выходному TOML файлу
Команды для сборки проекта и запуска тестов
Установка зависимостей:
pip install -r requirements.txt
Запуск:
python src/cli.py -o output.toml < examples/app_config.cfg
Запуск тестов:
python -m pytest tests/
Примеры использования
Пример 1: Конфигурация приложения (с вычислениями)
python src/cli.py -o app.toml < examples/app_config.cfg
Пример 2: Конфигурация игры (с вычислениями)
python src/cli.py -o game.toml < examples/game_settings.cfg
Результаты преобразования примеров
Пример 1: app_config.cfg → app.toml
Исходный файл с вычислениями:

% Конфигурация веб-приложения С ВЫЧИСЛЕНИЯМИ
app_name = [[Мое приложение]];
app_version = [[1.0.0]];

debug_mode = false;

% Вычисление уровня логирования
base_log_level = 2;
log_offset = 1;
log_level = $base_log_level log_offset +$;  % 2 + 1 = 3

% Настройки сервера с вычислениями
server = @{
    host = [[0.0.0.0]];
    base_port = 8000;
    port_offset = 80;
    port = $base_port port_offset +$;  % 8000 + 80 = 8080
    
    % Вычисление числа воркеров: (8080 / 1000) = 8
    workers = $port 1000 /$;
    
    ssl = @{
        enabled = true;
        cert_path = [[/etc/ssl/cert.pem]];
        
        % 8080 mod 443 = 8080 - (443 * 18) = 8080 - 7974 = 106
        ssl_check = $port 443 mod$;
    };
};

% Настройки базы данных с вычислениями
database = @{
    engine = [[postgresql]];
    host = [[localhost]];
    db_port = 5432;
    name = [[app_db]];
    
    % Вычисление: 8 * 12 = 96
    base_connections = $workers 12 *$;
    
    % Вычисление: 96 + 4 = 100
    max_connections = $base_connections 4 +$;
    
    % Путь вычисляется на основе порта
    connection_string = [[postgresql://localhost:5432/app_db]];
};
Результат преобразования (app.toml):

app_name = "Мое приложение"
app_version = "1.0.0"
debug_mode = false
log_level = 3

[server]
host = "0.0.0.0"
base_port = 8000
port_offset = 80
port = 8080
workers = 8

[server.ssl]
enabled = true
cert_path = "/etc/ssl/cert.pem"
ssl_check = 106

[database]
engine = "postgresql"
host = "localhost"
db_port = 5432
name = "app_db"
base_connections = 96
max_connections = 100
connection_string = "postgresql://localhost:5432/app_db"
Пример 2: game_settings.cfg → game.toml
Исходный файл с вычислениями:

% Настройки игры с вычислениями
game_title = [[Epic Adventure]];

% Вычисления для сложности
base_difficulty = 5;
difficulty_mod = 2;
game_difficulty = $base_difficulty difficulty_mod *$;  % 5 * 2 = 10

% Настройки графики
graphics = @{
    resolution = [[1920x1080]];
    base_fps = 60;
    
    % Вычисление: (10 * 6) = 60
    target_fps = $game_difficulty 6 *$;
    
    % Вычисление: 60 mod 30 = 0
    vsync_interval = $target_fps 30 mod$;
    
    effects = @{
        shadows = true;
        particles = $game_difficulty 2 /$;  % 10 / 2 = 5
    };
};

% Игровая механика
mechanics = @{
    % Вычисление начального здоровья: 100 - 10 = 90
    base_health = 100;
    health_penalty = $game_difficulty 1 *$;  % 10 * 1 = 10
    player_health = $base_health health_penalty -$;  % 100 - 10 = 90
    
    % Вычисления для урона
    base_damage = 20;
    damage_bonus = $game_difficulty 3 *$;  % 10 * 3 = 30
    weapon_damage = $base_damage damage_bonus +$;  % 20 + 30 = 50
};
Результат преобразования (game.toml):

game_title = "Epic Adventure"
game_difficulty = 10

[graphics]
resolution = "1920x1080"
base_fps = 60
target_fps = 60
vsync_interval = 0

[graphics.effects]
shadows = true
particles = 5

[mechanics]
base_health = 100
health_penalty = 10
player_health = 90
base_damage = 20
damage_bonus = 30
weapon_damage = 50
Структура проекта
.
├── examples/                    # Примеры конфигураций
│   ├── app_config.cfg          # Пример 1: конфигурация приложения
│   ├── game_settings.cfg       # Пример 2: настройки игры
│   ├── database.cfg            # Пример 3: база данных
│   └── complex_example.cfg     # Сложный пример
├── src/                        # Исходный код
│   ├── __init__.py
│   ├── cli.py                  # Интерфейс командной строки
│   ├── errors.py               # Обработка ошибок
│   ├── evaluator.py            # Вычислитель константных выражений
│   ├── lexer.py               # Лексер
│   ├── parser.py              # Парсер
│   └── transformer.py         # Преобразователь в TOML
├── tests/                      # Тесты
│   ├── test_evaluator.py
│   ├── test_integration.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_transformer.py
├── pyproject.toml             # Конфигурация проекта
├── requirements.txt           # Зависимости
└── README.md                  # Эта документация
История коммитов
Проект разрабатывался с использованием git. История коммитов отражает этапы разработки:

Базовый парсер и грамматика

Реализация константных вычислений

Добавление тестов

Документация и примеры
