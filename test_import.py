import sys
import os
print("=== ТЕСТ ИМПОРТА МОДУЛЕЙ ===")
# Добавляем текущую папку в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
print(f"Текущая папка: {current_dir}")
print(f"Файлы в папке: {os.listdir('.')}")
# Проверяем папку src
if os.path.exists('src'):
    print(f"\nФайлы в src/:")
    for f in os.listdir('src'):
        print(f"  {f}")
else:
    print("\n❌ Папка src/ не существует!")
print("\n=== ПРОВЕРКА ИМПОРТА ===")
# Попробуем импортировать напрямую
try:
    from src.jira_client import JiraClient
    print("✅ JiraClient импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта JiraClient: {e}")
try:
    from src.data_processor import calculate_open_time
    print("✅ calculate_open_time импортирована")
except ImportError as e:
    print(f"❌ Ошибка импорта calculate_open_time: {e}")
try:
    from src.plot_builder import plot_open_time_histogram
    print("✅ plot_open_time_histogram импортирована")
except ImportError as e:
    print(f"❌ Ошибка импорта plot_open_time_histogram: {e}")
print("\n=== ПРОВЕРКА СОДЕРЖИМОГО ФАЙЛОВ ===")
def check_file_content(filepath, required_strings):
    """Проверить наличие строк в файле"""
    if not os.path.exists(filepath):
        print(f"❌ Файл не существует: {filepath}")
        return False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        missing = []
        for req in required_strings:
            if req not in content:
                missing.append(req)
        if missing:
            print(f"⚠ В файле {filepath} отсутствуют: {missing}")
            return False
        else:
            print(f"✅ Файл {filepath} содержит нужные строки")
            return True
    except Exception as e:
        print(f"❌ Ошибка чтения {filepath}: {e}")
        return False
# Проверяем ключевые файлы
check_file_content('src/jira_client.py', ['class JiraClient', 'def get_issues'])
check_file_content('src/data_processor.py', ['def calculate_open_time', 'pd.DataFrame'])
check_file_content('src/plot_builder.py', ['def plot_open_time_histogram', 'plt.figure'])
print("\n=== ТЕСТ ЗАВЕРШЕН ===")
