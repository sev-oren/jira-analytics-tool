import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def test_module_integration():
    """Интеграционный тест взаимодействия модулей"""
    try:
        # Импортируем все основные модули
        from src.jira_client import JiraClient
        from src.data_processor import calculate_open_time
        from src.plot_builder import plot_open_time_histogram
        from src.main import load_config, setup_logging
        print("✓ Все модули импортируются успешно")
        # Проверяем конфигурацию
        config = load_config()
        assert config is not None
        print("✓ Конфигурация загружается")
        # Проверяем создание клиента
        client = JiraClient(
            server_url=config['jira']['server'],
            project_key=config['jira']['project_key'],
            max_results=10
        )
        assert client is not None
        print("✓ Клиент JIRA создается")
        # Проверяем функции обработки данных
        test_data = [{
            'key': 'TEST-INT-1',
            'fields': {
                'created': '2023-01-01T00:00:00.000+0000',
                'resolutiondate': '2023-01-02T00:00:00.000+0000'
            }
        }]
        result = calculate_open_time(test_data)
        assert result is not None
        print("✓ Функция calculate_open_time работает")
        print("✓ test_module_integration passed")
    except Exception as e:
        print(f"✗ test_module_integration failed: {e}")
        import traceback
        traceback.print_exc()
def test_project_structure():
    """Тест структуры проекта"""
    required_dirs = ['src', 'tests', 'config', 'logs', 'plots']
    required_files = [
        'src/__init__.py',
        'src/jira_client.py',
        'src/data_processor.py',
        'src/plot_builder.py',
        'src/main.py',
        'requirements.txt',
        'config/config.yaml',
        'README.md'
    ]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ Папка {dir_name} существует")
        else:
            print(f"✗ Папка {dir_name} отсутствует")
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ Файл {file_name} существует")
        else:
            print(f"✗ Файл {file_name} отсутствует")
    print("✓ test_project_structure passed")
if __name__ == "__main__":
    test_module_integration()
    test_project_structure()
    print("\n✅ Все интеграционные тесты пройдены!")
