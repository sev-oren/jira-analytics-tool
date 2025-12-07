#!/usr/bin/env python3
"""
Главный модуль JIRA Analytics Tool
"""
import sys
import os
import logging
import yaml
from pathlib import Path
print("=" * 60)
print("JIRA Analytics Tool - Запуск")
print("=" * 60)
# Добавляем путь для импорта модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
print(f"Python: {sys.executable}")
print(f"Текущая папка: {os.getcwd()}")
print(f"Путь к src: {current_dir}")
try:
    from src.jira_client import JiraClient
    from src.data_processor import calculate_open_time
    from src.plot_builder import plot_open_time_histogram
    print("OK: Основные модули импортированы")
except ImportError as e:
    print(f"ERROR: Ошибка импорта модулей: {e}")
    print("Проверьте наличие файлов в папке src/")
    sys.exit(1)
def setup_logging():
    """Настройка логирования"""
    # Сначала создаем папку logs
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    # Настраиваем логирование
    log_file = os.path.join(logs_dir, "jira_analytics.log")
    # Используем базовую кодировку для Windows
    handler = logging.FileHandler(log_file, encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            handler,
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Логирование настроено, файл: {log_file}")
    return logger
def load_config():
    """Загрузка конфигурации"""
    config_path = "config/config.yaml"
    print(f"Поиск конфигурации: {config_path}")
    if not os.path.exists(config_path):
        print(f"WARNING: Файл конфигурации не найден, используются настройки по умолчанию")
        config = {
            'jira': {
                'server': 'https://issues.apache.org/jira',
                'project_key': 'KAFKA',
                'max_results': 50
            },
            'plots': {
                'output_dir': 'plots',
                'top_users_count': 30
            }
        }
        return config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            print("WARNING: Файл конфигурации пуст, используются настройки по умолчанию")
            config = {
                'jira': {
                    'server': 'https://issues.apache.org/jira',
                    'project_key': 'KAFKA',
                    'max_results': 50
                },
                'plots': {
                    'output_dir': 'plots',
                    'top_users_count': 30
                }
            }
            return config
        config = yaml.safe_load(content)
        if config is None:
            print("WARNING: Файл конфигурации содержит только комментарии, используются настройки по умолчанию")
            config = {
                'jira': {
                    'server': 'https://issues.apache.org/jira',
                    'project_key': 'KAFKA',
                    'max_results': 50
                },
                'plots': {
                    'output_dir': 'plots',
                    'top_users_count': 30
                }
            }
        print("OK: Конфигурация загружена")
        return config
    except yaml.YAMLError as e:
        print(f"ERROR: Ошибка формата YAML: {e}")
        print("WARNING: Используются настройки по умолчанию")
        config = {
            'jira': {
                'server': 'https://issues.apache.org/jira',
                'project_key': 'KAFKA',
                'max_results': 50
            },
            'plots': {
                'output_dir': 'plots',
                'top_users_count': 30
            }
        }
        return config
    except Exception as e:
        print(f"ERROR: Ошибка загрузки конфигурации: {e}")
        print("WARNING: Используются настройки по умолчанию")
        config = {
            'jira': {
                'server': 'https://issues.apache.org/jira',
                'project_key': 'KAFKA',
                'max_results': 50
            },
            'plots': {
                'output_dir': 'plots',
                'top_users_count': 30
            }
        }
        return config
def main():
    """Основная функция"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Запуск JIRA Analytics Tool")
    logger.info("=" * 60)
    # Загрузка конфигурации
    config = load_config()
    # Создание папок
    Path("logs").mkdir(exist_ok=True)
    Path("plots").mkdir(exist_ok=True)
    print("OK: Папки logs/ и plots/ созданы")
    # Инициализация клиента JIRA
    jira_config = config['jira']
    client = JiraClient(
        server_url=jira_config['server'],
        project_key=jira_config['project_key'],
        max_results=jira_config.get('max_results', 50)
    )
    print(f"OK: Клиент JIRA создан")
    print(f"  Сервер: {jira_config['server']}")
    print(f"  Проект: {jira_config['project_key']}")
    # Получение данных
    jql = f"project = {jira_config['project_key']} AND status = Closed"
    print(f"JQL запрос: {jql}")
    print("Получение данных из JIRA...")
    issues = client.get_issues(jql)
    if not issues:
        logger.error("Не получено ни одной задачи")
        print("ERROR: Не получено ни одной задачи. Возможные причины:")
        print("  1. Нет интернет-соединения")
        print("  2. Проект не существует или нет закрытых задач")
        print("  3. Проблемы с доступом к JIRA API")
        return
    print(f"OK: Получено задач: {len(issues)}")
    # Обработка данных
    print("Обработка данных...")
    df = calculate_open_time(issues)
    if df.empty:
        logger.warning("Нет данных для построения графиков")
        print("WARNING: Нет данных для построения графиков")
        return
    print(f"OK: Обработано задач для графика: {len(df)}")
    # Построение графиков
    print("Построение графика...")
    output_path = "plots/open_time_histogram.png"
    try:
        plot_open_time_histogram(df, output_path)
        print(f"OK: График сохранен: {output_path}")
        # Покажем статистику
        print("\nСтатистика времени в открытом состоянии:")
        print(f"   Минимум: {df['open_hours'].min():.1f} часов")
        print(f"   Максимум: {df['open_hours'].max():.1f} часов")
        print(f"   Среднее: {df['open_hours'].mean():.1f} часов")
        print(f"   Медиана: {df['open_hours'].median():.1f} часов")
    except Exception as e:
        print(f"ERROR: Ошибка при построении графика: {e}")
        import traceback
        traceback.print_exc()
    print("\n" + "=" * 60)
    print("OK: Выполнение завершено!")
    print("=" * 60)
    # Покажем где файлы
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / 1024
        print(f"Файл графика: {output_path} ({file_size:.1f} KB)")
    print(f"Логи: logs/jira_analytics.log")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"\nERROR: Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
