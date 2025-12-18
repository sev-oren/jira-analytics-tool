"""
Пакет для анализа JIRA задач
"""

__version__ = "1.0.0"
__author__ = "Ваше Имя"

# Экспортируем основные классы и функции для удобного импорта
from .jira_client import JiraClient
from .data_processor import (
    calculate_open_time,
    calculate_status_time_distribution,
    calculate_daily_issues_stats,
    calculate_top_users,
    calculate_time_spent_distribution,
    calculate_priority_distribution
)
from .plot_builder import (
    plot_open_time_histogram,
    plot_status_time_distributions,
    plot_daily_issues_chart,
    plot_top_users_chart,
    plot_time_spent_histogram,
    plot_priority_distribution_chart
)

# Можно определить __all__ для контроля импорта через from src import *
__all__ = [
    'JiraClient',
    'calculate_open_time',
    'calculate_status_time_distribution',
    'calculate_daily_issues_stats',
    'calculate_top_users',
    'calculate_time_spent_distribution',
    'calculate_priority_distribution',
    'plot_open_time_histogram',
    'plot_status_time_distributions',
    'plot_daily_issues_chart',
    'plot_top_users_chart',
    'plot_time_spent_histogram',
    'plot_priority_distribution_chart'
]

print(f"Инициализация пакета jira_analytics версии {__version__}")