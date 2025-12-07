import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from typing import List, Dict
from src.data_processor import calculate_open_time
def test_calculate_open_time_empty_list():
    """Тест с пустым списком задач"""
    issues: List[Dict] = []
    result = calculate_open_time(issues)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    print("✓ test_calculate_open_time_empty_list passed")
def test_calculate_open_time_single_issue():
    """Тест с одной задачей"""
    issues: List[Dict] = [{
        'key': 'TEST-1',
        'fields': {
            'created': '2023-01-01T10:00:00.000+0000',
            'resolutiondate': '2023-01-02T10:00:00.000+0000'
        }
    }]
    result = calculate_open_time(issues)
    assert len(result) == 1
    assert result.iloc[0]['key'] == 'TEST-1'
    # 24 часа разницы
    assert abs(result.iloc[0]['open_hours'] - 24.0) < 0.1
    print("✓ test_calculate_open_time_single_issue passed")
def test_calculate_open_time_missing_dates():
    """Тест с задачами без дат"""
    issues: List[Dict] = [
        {
            'key': 'TEST-2',
            'fields': {
                'created': '2023-01-01T10:00:00.000+0000',
                'resolutiondate': None  # Нет даты закрытия
            }
        },
        {
            'key': 'TEST-3',
            'fields': {
                'created': None,  # Нет даты создания
                'resolutiondate': '2023-01-02T10:00:00.000+0000'
            }
        }
    ]
    result = calculate_open_time(issues)
    assert len(result) == 0  # Обе задачи должны быть пропущены
    print("✓ test_calculate_open_time_missing_dates passed")
def test_calculate_open_time_multiple_issues():
    """Тест с несколькими задачами"""
    issues: List[Dict] = [
        {
            'key': 'TEST-4',
            'fields': {
                'created': '2023-01-01T00:00:00.000+0000',
                'resolutiondate': '2023-01-01T12:00:00.000+0000'  # 12 часов
            }
        },
        {
            'key': 'TEST-5',
            'fields': {
                'created': '2023-01-01T00:00:00.000+0000',
                'resolutiondate': '2023-01-02T00:00:00.000+0000'  # 24 часа
            }
        },
        {
            'key': 'TEST-6',
            'fields': {
                'created': '2023-01-01T00:00:00.000+0000',
                'resolutiondate': '2023-01-03T00:00:00.000+0000'  # 48 часов
            }
        }
    ]
    result = calculate_open_time(issues)
    assert len(result) == 3
    assert set(result['key'].tolist()) == {'TEST-4', 'TEST-5', 'TEST-6'}
    assert abs(result[result['key'] == 'TEST-4']['open_hours'].iloc[0] - 12.0) < 0.1
    assert abs(result[result['key'] == 'TEST-5']['open_hours'].iloc[0] - 24.0) < 0.1
    assert abs(result[result['key'] == 'TEST-6']['open_hours'].iloc[0] - 48.0) < 0.1
    print("✓ test_calculate_open_time_multiple_issues passed")
def test_calculate_open_time_dataframe_structure():
    """Тест структуры возвращаемого DataFrame"""
    issues: List[Dict] = [{
        'key': 'TEST-7',
        'fields': {
            'created': '2023-01-01T00:00:00.000+0000',
            'resolutiondate': '2023-01-02T00:00:00.000+0000'
        }
    }]
    result = calculate_open_time(issues)
    expected_columns = ['key', 'created', 'resolved', 'open_hours', 'days']
    for col in expected_columns:
        assert col in result.columns
    print("✓ test_calculate_open_time_dataframe_structure passed")
if __name__ == "__main__":
    test_calculate_open_time_empty_list()
    test_calculate_open_time_single_issue()
    test_calculate_open_time_missing_dates()
    test_calculate_open_time_multiple_issues()
    test_calculate_open_time_dataframe_structure()
    print("\n✅ Все тесты DataProcessor пройдены!")
