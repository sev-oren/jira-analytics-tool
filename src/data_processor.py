import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import logging
from dateutil import parser  # Нужна для парсинга сложных форматов дат
logger = logging.getLogger(__name__)
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
                continue  # Пропускаем задачи без дат
            # Используем dateutil.parser для сложных форматов дат
            # Он лучше обрабатывает различные форматы
            created_dt = parser.isoparse(created) if hasattr(parser, 'isoparse') else parser.parse(created)
            resolved_dt = parser.isoparse(resolved) if hasattr(parser, 'isoparse') else parser.parse(resolved)
            # Вычисляем разницу в часах
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
            # Выводим только первые 5 ошибок
            if error_count <= 5:
                print(f"Ошибка обработки задачи {key}: {e}")
            continue
    if data:
        df = pd.DataFrame(data)
        print(f"Успешно обработано: {processed_count} из {len(issues)} задач")
        if error_count > 0:
            print(f"Ошибок при обработке: {error_count}")
        # Базовая статистика
        print(f"Статистика времени в открытом состоянии:")
        print(f"  • Минимум: {df['open_hours'].min():.1f} часов ({df['open_hours'].min()/24:.1f} дней)")
        print(f"  • Максимум: {df['open_hours'].max():.1f} часов ({df['open_hours'].max()/24:.1f} дней)")
        print(f"  • Среднее: {df['open_hours'].mean():.1f} часов ({df['open_hours'].mean()/24:.1f} дней)")
        print(f"  • Медиана: {df['open_hours'].median():.1f} часов ({df['open_hours'].median()/24:.1f} дней)")
        return df
    else:
        print("Не удалось обработать ни одной задачи")
        return pd.DataFrame()
# Остальные функции остаются без изменений...
