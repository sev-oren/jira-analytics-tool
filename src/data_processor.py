import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging
from dateutil import parser
from collections import defaultdict, Counter
logger = logging.getLogger(__name__)
# ===== ФУНКЦИЯ 1: Время в открытом состоянии (ГОТОВО) =====
def calculate_open_time(issues: List[Dict]) -> pd.DataFrame:
    """Рассчитать время в открытом состоянии (от создания до закрытия)"""
    data = []
    if not issues:
        print("Внимание: Нет задач для обработки")
        return pd.DataFrame()
    print(f"Начало обработки {len(issues)} задач...")
    processed_count = 0
    error_count = 0
    for issue in issues:
        try:
            fields = issue.get('fields', {})
            key = issue.get('key', 'UNKNOWN')
            created = fields.get('created')
            resolved = fields.get('resolutiondate')
            if not created or not resolved:
                continue
            created_dt = parser.isoparse(created) if hasattr(parser, 'isoparse') else parser.parse(created)
            resolved_dt = parser.isoparse(resolved) if hasattr(parser, 'isoparse') else parser.parse(resolved)
            open_hours = (resolved_dt - created_dt).total_seconds() / 3600
            data.append({
                'key': key,
                'created': created_dt,
                'resolved': resolved_dt,
                'open_hours': open_hours,
                'days': open_hours / 24
            })
            processed_count += 1
        except Exception as e:
            error_count += 1
            continue
    if data:
        df = pd.DataFrame(data)
        print(f"Успешно обработано: {processed_count} из {len(issues)} задач")
        return df
    else:
        print("Не удалось обработать ни одной задачи")
        return pd.DataFrame()
# ===== ФУНКЦИЯ 2: Распределение по приоритетам =====
def calculate_priority_distribution(issues: List[Dict]) -> pd.DataFrame:
    """Рассчитать распределение задач по приоритетам"""
    priority_count = {}
    for issue in issues:
        try:
            priority = issue['fields'].get('priority', {})
            if priority:
                priority_name = priority.get('name', 'Unknown')
                priority_count[priority_name] = priority_count.get(priority_name, 0) + 1
        except:
            continue
    if priority_count:
        df = pd.DataFrame({
            'priority': list(priority_count.keys()),
            'count': list(priority_count.values())
        }).sort_values('count', ascending=False)
        print(f"Найдено приоритетов: {len(df)}")
        return df
    return pd.DataFrame()
# ===== ФУНКЦИЯ 3: Топ пользователей =====
def calculate_top_users(issues: List[Dict], top_n: int = 30) -> pd.DataFrame:
    """Топ пользователей (исполнитель и репортер)"""
    user_stats = defaultdict(lambda: {'reporter': 0, 'assignee': 0, 'total': 0})
    for issue in issues:
        try:
            fields = issue['fields']
            # Репортер
            reporter = fields.get('reporter')
            if reporter:
                reporter_name = reporter.get('displayName', reporter.get('name', 'Unknown'))
                user_stats[reporter_name]['reporter'] += 1
                user_stats[reporter_name]['total'] += 1
            # Исполнитель
            assignee = fields.get('assignee')
            if assignee:
                assignee_name = assignee.get('displayName', assignee.get('name', 'Unknown'))
                user_stats[assignee_name]['assignee'] += 1
                user_stats[assignee_name]['total'] += 1
        except Exception as e:
            continue
    if user_stats:
        data = []
        for user, stats in user_stats.items():
            data.append({
                'user': user,
                'as_reporter': stats['reporter'],
                'as_assignee': stats['assignee'],
                'total_tasks': stats['total']
            })
        df = pd.DataFrame(data)
        df = df.sort_values('total_tasks', ascending=False).head(top_n)
        print(f"Найдено пользователей: {len(user_stats)}, топ {top_n}")
        return df
    return pd.DataFrame()
# ===== ФУНКЦИЯ 4: Статистика по дням =====
def calculate_daily_issues_stats(issues: List[Dict]) -> pd.DataFrame:
    """Рассчитать статистику по дням (с накопительным итогом)"""
    daily_created = defaultdict(int)
    daily_resolved = defaultdict(int)
    for issue in issues:
        try:
            fields = issue['fields']
            # Созданные задачи
            created = fields.get('created')
            if created:
                created_dt = parser.isoparse(created) if hasattr(parser, 'isoparse') else parser.parse(created)
                created_date = created_dt.date()
                daily_created[created_date] += 1
            # Закрытые задачи
            resolved = fields.get('resolutiondate')
            if resolved:
                resolved_dt = parser.isoparse(resolved) if hasattr(parser, 'isoparse') else parser.parse(resolved)
                resolved_date = resolved_dt.date()
                daily_resolved[resolved_date] += 1
        except Exception:
            continue
    if not daily_created and not daily_resolved:
        return pd.DataFrame()
    # Объединяем все даты
    all_dates = set(list(daily_created.keys()) + list(daily_resolved.keys()))
    all_dates = sorted(list(all_dates))
    data = []
    created_cumulative = 0
    resolved_cumulative = 0
    for date in all_dates:
        created_today = daily_created.get(date, 0)
        resolved_today = daily_resolved.get(date, 0)
        created_cumulative += created_today
        resolved_cumulative += resolved_today
        data.append({
            'date': date,
            'created_today': created_today,
            'resolved_today': resolved_today,
            'created_cumulative': created_cumulative,
            'resolved_cumulative': resolved_cumulative,
            'open_cumulative': created_cumulative - resolved_cumulative
        })
    df = pd.DataFrame(data)
    print(f"Статистика по {len(df)} дням")
    return df
# ===== ФУНКЦИЯ 5: Затраченное время =====
def calculate_time_spent_distribution(issues: List[Dict]) -> pd.DataFrame:
    """Распределение затраченного времени (на основе logged time)"""
    time_spent_data = []
    for issue in issues:
        try:
            fields = issue['fields']
            key = issue['key']
            # Время из поля timespent (в секундах)
            timespent = fields.get('timespent')
            if timespent:
                hours = timespent / 3600  # Конвертируем в часы
                time_spent_data.append({
                    'key': key,
                    'hours_spent': hours,
                    'days_spent': hours / 24
                })
        except Exception:
            continue
    if time_spent_data:
        df = pd.DataFrame(time_spent_data)
        print(f"Найдено задач с logged time: {len(df)}")
        return df
    return pd.DataFrame()
# ===== ФУНКЦИЯ 6: Распределение по состояниям =====
def calculate_status_time_distribution(issues: List[Dict]) -> pd.DataFrame:
    """Распределение времени по состояниям задачи (упрощенная версия)"""
    status_data = []
    for issue in issues:
        try:
            fields = issue['fields']
            key = issue['key']
            # Текущий статус
            status = fields.get('status', {}).get('name', 'Unknown')
            # Время в открытом состоянии (из уже рассчитанного)
            created = fields.get('created')
            resolved = fields.get('resolutiondate')
            if created and resolved:
                created_dt = parser.isoparse(created) if hasattr(parser, 'isoparse') else parser.parse(created)
                resolved_dt = parser.isoparse(resolved) if hasattr(parser, 'isoparse') else parser.parse(resolved)
                open_hours = (resolved_dt - created_dt).total_seconds() / 3600
                status_data.append({
                    'key': key,
                    'status': status,
                    'hours_in_status': open_hours
                })
        except Exception:
            continue
    if status_data:
        df = pd.DataFrame(status_data)
        print(f"Статусы обработаны для {len(df)} задач")
        return df
    return pd.DataFrame()
