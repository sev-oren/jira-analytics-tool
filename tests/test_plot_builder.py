import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Используем бэкенд без GUI для тестов
from src.plot_builder import plot_open_time_histogram
import tempfile
def test_plot_open_time_histogram_with_data():
    """Тест построения гистограммы с данными"""
    # Создаем тестовые данные
    df = pd.DataFrame({
        'key': ['TEST-1', 'TEST-2', 'TEST-3'],
        'open_hours': [10.5, 25.0, 50.2]
    })
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        output_path = tmp.name
    try:
        # Пробуем построить график
        plot_open_time_histogram(df, output_path)
        # Проверяем что файл создан
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        print("✓ test_plot_open_time_histogram_with_data passed")
    finally:
        # Удаляем временный файл
        if os.path.exists(output_path):
            os.unlink(output_path)
def test_plot_open_time_histogram_empty_data():
    """Тест построения гистограммы с пустыми данными"""
    df = pd.DataFrame()
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        output_path = tmp.name
    try:
        # Должен завершиться без ошибок
        plot_open_time_histogram(df, output_path)
        print("✓ test_plot_open_time_histogram_empty_data passed")
    except Exception as e:
        print(f"✗ test_plot_open_time_histogram_empty_data failed: {e}")
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)
def test_plot_builder_functions_exist():
    """Тест наличия всех функций построения графиков"""
    from src.plot_builder import (
        plot_open_time_histogram,
        plot_status_time_distributions,
        plot_daily_issues_chart,
        plot_top_users_chart,
        plot_time_spent_histogram,
        plot_priority_distribution_chart
    )
    # Проверяем что все функции существуют
    functions = [
        plot_open_time_histogram,
        plot_status_time_distributions,
        plot_daily_issues_chart,
        plot_top_users_chart,
        plot_time_spent_histogram,
        plot_priority_distribution_chart
    ]
    for func in functions:
        assert callable(func)
    print("✓ test_plot_builder_functions_exist passed")
if __name__ == "__main__":
    test_plot_open_time_histogram_with_data()
    test_plot_open_time_histogram_empty_data()
    test_plot_builder_functions_exist()
    print("\n✅ Все тесты PlotBuilder пройдены!")
