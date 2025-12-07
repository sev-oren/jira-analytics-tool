import sys
import os
print("=== ПРОСТОЙ ТЕСТ ЗАПУСКА ===")
# Проверка импорта основных модулей
try:
    from src.jira_client import JiraClient
    from src.data_processor import calculate_open_time
    from src.plot_builder import plot_open_time_histogram
    print("✓ Модули импортированы")
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    sys.exit(1)
# Проверка работы функций
print("\n=== ТЕСТ ФУНКЦИЙ ===")
# Тестовые данные
test_issues = [
    {
        'key': 'TEST-1',
        'fields': {
            'created': '2023-01-01T10:00:00.000+0000',
            'resolutiondate': '2023-01-02T10:00:00.000+0000',
            'priority': {'name': 'Major'},
            'reporter': {'displayName': 'Test User'},
            'status': {'name': 'Closed'}
        }
    }
]
# Тест calculate_open_time
try:
    df = calculate_open_time(test_issues)
    print(f"✓ calculate_open_time: обработано {len(df)} задач")
except Exception as e:
    print(f"✗ calculate_open_time: {e}")
# Тест построения графика
try:
    import os
    os.makedirs('test_plots', exist_ok=True)
    if not df.empty:
        plot_open_time_histogram(df, 'test_plots/test_histogram.png')
        if os.path.exists('test_plots/test_histogram.png'):
            print("✓ График создан: test_plots/test_histogram.png")
        else:
            print("✗ График не создан")
    else:
        print("✗ Нет данных для графика")
except Exception as e:
    print(f"✗ Ошибка построения графика: {e}")
print("\n=== ТЕСТ ЗАВЕРШЕН ===")
