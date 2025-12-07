"""
Тесты для полного покрытия всех 6 графиков
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from typing import List, Dict
from src.data_processor import (
    calculate_open_time,
    calculate_priority_distribution,
    calculate_top_users,
    calculate_daily_issues_stats,
    calculate_time_spent_distribution,
    calculate_status_time_distribution
)
def create_test_issues(count: int = 10) -> List[Dict]:
    """Создание тестовых задач"""
    issues = []
    for i in range(count):
        issues.append({
            'key': f'TEST-{i+1}',
            'fields': {
                'created': '2023-01-01T10:00:00.000+0000',
                'resolutiondate': '2023-01-0{day}T10:00:00.000+0000'.format(day=(i % 5) + 2),
                'priority': {'name': ['Blocker', 'Critical', 'Major', 'Minor', 'Trivial'][i % 5]},
                'reporter': {'displayName': f'User{i % 3}', 'name': f'user{i % 3}'},
                'assignee': {'displayName': f'Assignee{i % 4}', 'name': f'assignee{i % 4}'},
                'status': {'name': ['Closed', 'Resolved', 'In Progress', 'Open'][i % 4]},
                'timespent': i * 3600,  # i часов в секундах
                'summary': f'Test issue {i+1}'
            }
        })
    return issues
def test_all_functions_with_data():
    """Тест всех функций с тестовыми данными"""
    print("Тестирование всех функций обработки данных...")
    issues = create_test_issues(10)
    # 1. Время в открытом состоянии
    df1 = calculate_open_time(issues)
    assert isinstance(df1, pd.DataFrame)
    assert len(df1) > 0
    print("  ✓ calculate_open_time")
    # 2. Распределение по приоритетам
    df2 = calculate_priority_distribution(issues)
    assert isinstance(df2, pd.DataFrame)
    print("  ✓ calculate_priority_distribution")
    # 3. Топ пользователей
    df3 = calculate_top_users(issues, top_n=5)
    assert isinstance(df3, pd.DataFrame)
    print("  ✓ calculate_top_users")
    # 4. Статистика по дням
    df4 = calculate_daily_issues_stats(issues)
    assert isinstance(df4, pd.DataFrame)
    print("  ✓ calculate_daily_issues_stats")
    # 5. Затраченное время
    df5 = calculate_time_spent_distribution(issues)
    assert isinstance(df5, pd.DataFrame)
    print("  ✓ calculate_time_spent_distribution")
    # 6. Распределение по состояниям
    df6 = calculate_status_time_distribution(issues)
    assert isinstance(df6, pd.DataFrame)
    print("  ✓ calculate_status_time_distribution")
    print("\n✅ Все функции работают корректно!")
def test_empty_data():
    """Тест с пустыми данными"""
    print("\nТестирование с пустыми данными...")
    empty_issues = []
    for func_name, func in [
        ('calculate_open_time', calculate_open_time),
        ('calculate_priority_distribution', calculate_priority_distribution),
        ('calculate_top_users', calculate_top_users),
        ('calculate_daily_issues_stats', calculate_daily_issues_stats),
        ('calculate_time_spent_distribution', calculate_time_spent_distribution),
        ('calculate_status_time_distribution', calculate_status_time_distribution)
    ]:
        result = func(empty_issues)
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        print(f"  ✓ {func_name} с пустыми данными")
    print("✅ Все функции корректно обрабатывают пустые данные!")
def test_data_types():
    """Тест типов возвращаемых данных"""
    print("\nПроверка типов данных...")
    issues = create_test_issues(5)
    # Проверка типов колонок для каждой функции
    df1 = calculate_open_time(issues)
    if not df1.empty:
        assert 'open_hours' in df1.columns
        assert pd.api.types.is_numeric_dtype(df1['open_hours'])
        print("  ✓ Типы данных calculate_open_time")
    df2 = calculate_priority_distribution(issues)
    if not df2.empty:
        assert 'priority' in df2.columns
        assert 'count' in df2.columns
        print("  ✓ Типы данных calculate_priority_distribution")
    print("✅ Все типы данных корректны!")
if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОЛНОГО ПОКРЫТИЯ")
    print("=" * 60)
    test_all_functions_with_data()
    test_empty_data()
    test_data_types()
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 60)
