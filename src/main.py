#!/usr/bin/env python3
"""
Главный модуль JIRA Analytics Tool - Полная версия с 6 графиками
"""
import sys
import os
import logging
import yaml
from pathlib import Path
print("=" * 60)
print("JIRA Analytics Tool - Полная версия с 6 графиками")
print("=" * 60)
# Добавляем путь для импорта модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
print(f"Python: {sys.executable}")
print(f"Текущая папка: {os.getcwd()}")
try:
    from src.jira_client import JiraClient
    from src.data_processor import (
        calculate_open_time,
        calculate_priority_distribution,
        calculate_top_users,
        calculate_daily_issues_stats,
        calculate_time_spent_distribution,
        calculate_status_time_distribution
    )
    from src.plot_builder import (
        plot_open_time_histogram,
        plot_priority_distribution_chart,
        plot_top_users_chart,
        plot_daily_issues_chart,
        plot_time_spent_histogram,
        plot_status_time_distributions
    )
    print("OK: Все модули импортированы")
except ImportError as e:
    print(f"ERROR: Ошибка импорта модулей: {e}")
    sys.exit(1)
def setup_logging():
    """Настройка логирования"""
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, "jira_analytics.log")
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
    logger.info(f"Логирование настроено")
    return logger
def load_config():
    """Загрузка конфигурации"""
    config_path = "config/config.yaml"
    print(f"Поиск конфигурации: {config_path}")
    if not os.path.exists(config_path):
        print(f"WARNING: Файл конфигурации не найден, используются настройки по умолчанию")
        return get_default_config()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            print("WARNING: Файл конфигурации пуст")
            return get_default_config()
        config = yaml.safe_load(content)
        if config is None:
            print("WARNING: Файл конфигурации содержит только комментарии")
            return get_default_config()
        print("OK: Конфигурация загружена")
        return config
    except yaml.YAMLError as e:
        print(f"ERROR: Ошибка формата YAML: {e}")
        return get_default_config()
    except Exception as e:
        print(f"ERROR: Ошибка загрузки конфигурации: {e}")
        return get_default_config()
def get_default_config():
    """Конфигурация по умолчанию"""
    return {
        'jira': {
            'server': 'https://issues.apache.org/jira',
            'project_key': 'KAFKA',
            'max_results': 200
        },
        'plots': {
            'output_dir': 'plots',
            'top_users_count': 30
        }
    }
def build_all_plots(issues, config):
    """Построение всех 6 графиков"""
    plots_config = config.get('plots', {})
    output_dir = plots_config.get('output_dir', 'plots')
    top_users_count = plots_config.get('top_users_count', 30)
    # Создаем папку для графиков
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\n{'='*60}")
    print("НАЧАЛО ПОСТРОЕНИЯ ГРАФИКОВ")
    print(f"{'='*60}")
    results = {}
    # === ГРАФИК 1: Гистограмма времени в открытом состоянии ===
    print("\n1. Гистограмма времени в открытом состоянии...")
    open_time_df = calculate_open_time(issues)
    if not open_time_df.empty:
        output_path = f"{output_dir}/1_open_time_histogram.png"
        plot_open_time_histogram(open_time_df, output_path)
        results['open_time'] = {'path': output_path, 'tasks': len(open_time_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    # === ГРАФИК 2: Распределение по приоритетам ===
    print("\n2. Распределение по приоритетам...")
    priority_df = calculate_priority_distribution(issues)
    if not priority_df.empty:
        output_path = f"{output_dir}/2_priority_distribution.png"
        plot_priority_distribution_chart(priority_df, output_path)
        results['priority'] = {'path': output_path, 'priorities': len(priority_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    # === ГРАФИК 3: Топ пользователей ===
    print("\n3. Топ пользователей...")
    users_df = calculate_top_users(issues, top_users_count)
    if not users_df.empty:
        output_path = f"{output_dir}/3_top_users.png"
        plot_top_users_chart(users_df, output_path)
        results['top_users'] = {'path': output_path, 'users': len(users_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    # === ГРАФИК 4: Статистика по дням ===
    print("\n4. Статистика по дням...")
    daily_df = calculate_daily_issues_stats(issues)
    if not daily_df.empty:
        output_path = f"{output_dir}/4_daily_stats.png"
        plot_daily_issues_chart(daily_df, output_path)
        results['daily'] = {'path': output_path, 'days': len(daily_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    # === ГРАФИК 5: Затраченное время ===
    print("\n5. Затраченное время...")
    time_spent_df = calculate_time_spent_distribution(issues)
    if not time_spent_df.empty:
        output_path = f"{output_dir}/5_time_spent.png"
        plot_time_spent_histogram(time_spent_df, output_path)
        results['time_spent'] = {'path': output_path, 'tasks': len(time_spent_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    # === ГРАФИК 6: Распределение по состояниям ===
    print("\n6. Распределение по состояниям...")
    status_df = calculate_status_time_distribution(issues)
    if not status_df.empty:
        output_path = f"{output_dir}/6_status_distribution.png"
        plot_status_time_distributions(status_df, output_path)
        results['status'] = {'path': output_path, 'tasks': len(status_df)}
        print(f"   OK: Сохранен: {output_path}")
    else:
        print("   WARNING: Нет данных")
    return results
def main():
    """Основная функция"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Запуск JIRA Analytics Tool - полная версия")
    logger.info("=" * 60)
    # Загрузка конфигурации
    config = load_config()
    # Создание папок
    Path("logs").mkdir(exist_ok=True)
    print("OK: Папки logs/ создана")
    # Инициализация клиента JIRA
    jira_config = config['jira']
    client = JiraClient(
        server_url=jira_config['server'],
        project_key=jira_config['project_key'],
        max_results=jira_config.get('max_results', 200)
    )
    print(f"OK: Клиент JIRA создан")
    print(f"   Сервер: {jira_config['server']}")
    print(f"   Проект: {jira_config['project_key']}")
    print(f"   Макс. задач: {jira_config.get('max_results', 200)}")
    # Получение данных
    jql = f"project = {jira_config['project_key']} AND status = Closed"
    print(f"\nJQL запрос: {jql}")
    print("\nПолучение данных из JIRA...")
    issues = client.get_issues(jql)
    if not issues:
        logger.error("Не получено ни одной задачи")
        print("ERROR: Не получено ни одной задачи")
        return
    print(f"OK: Получено задач: {len(issues)}")
    # Построение всех графиков
    results = build_all_plots(issues, config)
    # Итоговая статистика
    print(f"\n{'='*60}")
    print("ИТОГ ПОСТРОЕНИЯ ГРАФИКОВ")
    print(f"{'='*60}")
    successful_plots = sum(1 for r in results.values() if 'path' in r)
    print(f"\nУспешно построено графиков: {successful_plots} из 6")
    if successful_plots > 0:
        print("\nСозданные графики:")
        for plot_name, plot_data in results.items():
            if 'path' in plot_data:
                path = plot_data['path']
                if os.path.exists(path):
                    size_kb = os.path.getsize(path) / 1024
                    print(f"  * {plot_name}: {path} ({size_kb:.1f} KB)")
    print(f"\n{'='*60}")
    print("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО!")
    print(f"{'='*60}")
    print(f"\nЛоги: logs/jira_analytics.log")
    print(f"Графики: plots/")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"\nERROR: Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()