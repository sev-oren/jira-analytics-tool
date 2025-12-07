import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def test_main_module_import():
    """Тест импорта главного модуля"""
    try:
        from src import main
        assert hasattr(main, 'main')
        assert callable(main.main)
        print("✓ test_main_module_import passed")
    except ImportError as e:
        print(f"✗ test_main_module_import failed: {e}")
def test_config_loading():
    """Тест загрузки конфигурации"""
    try:
        from src.main import load_config
        config = load_config()
        # Проверяем базовую структуру конфигурации
        assert isinstance(config, dict)
        assert 'jira' in config
        assert 'server' in config['jira']
        assert 'project_key' in config['jira']
        print("✓ test_config_loading passed")
    except Exception as e:
        print(f"✗ test_config_loading failed: {e}")
def test_logging_setup():
    """Тест настройки логирования"""
    try:
        from src.main import setup_logging
        import logging
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)
        print("✓ test_logging_setup passed")
    except Exception as e:
        print(f"✗ test_logging_setup failed: {e}")
if __name__ == "__main__":
    test_main_module_import()
    test_config_loading()
    test_logging_setup()
    print("\n✅ Все тесты Main module пройдены!")
