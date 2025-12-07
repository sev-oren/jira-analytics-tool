import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np
from typing import Optional
import matplotlib
# Используем агрессивный бэкенд для серверов
matplotlib.use('Agg')
# Настройки стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
# ===== ГРАФИК 1: Гистограмма времени в открытом состоянии (ГОТОВО) =====
def plot_open_time_histogram(df: pd.DataFrame, output_path: str):
    """Построить гистограмму времени в открытом состоянии"""
    if df.empty:
        print("Нет данных для гистограммы")
        return
    print(f"Создание гистограммы: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    # 1. Гистограмма с KDE
    sns.histplot(data=df, x='open_hours', bins=30, kde=True, ax=ax1)
    mean_val = df['open_hours'].mean()
    median_val = df['open_hours'].median()
    ax1.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                label=f'Среднее: {mean_val:.1f} ч')
    ax1.axvline(median_val, color='green', linestyle=':', linewidth=2,
                label=f'Медиана: {median_val:.1f} ч')
    ax1.set_title(f'Гистограмма времени в открытом состоянии\nВсего задач: {len(df)}', fontsize=14)
    ax1.set_xlabel('Часы в открытом состоянии', fontsize=12)
    ax1.set_ylabel('Количество задач', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    # 2. Box plot
    sns.boxplot(data=df, y='open_hours', ax=ax2)
    ax2.set_title('Распределение времени (Box Plot)', fontsize=14)
    ax2.set_ylabel('Часы в открытом состоянии', fontsize=12)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Гистограмма сохранена: {output_path}")
# ===== ГРАФИК 2: Распределение по приоритетам =====
def plot_priority_distribution_chart(priority_data: pd.DataFrame, output_path: str):
    """Распределение задач по приоритетам"""
    if priority_data.empty:
        print("Нет данных для графика приоритетов")
        return
    print(f"Создание графика приоритетов: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(12, 6))
    # Строим столбчатую диаграмму
    bars = plt.bar(priority_data['priority'], priority_data['count'], color='skyblue')
    plt.title(f'Распределение задач по приоритетам\nВсего задач: {priority_data["count"].sum()}', fontsize=14)
    plt.xlabel('Приоритет', fontsize=12)
    plt.ylabel('Количество задач', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    # Добавляем значения на столбцы
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"График приоритетов сохранен: {output_path}")
# ===== ГРАФИК 3: Топ пользователей =====
def plot_top_users_chart(top_users: pd.DataFrame, output_path: str):
    """График топ пользователей"""
    if top_users.empty:
        print("Нет данных для графика пользователей")
        return
    print(f"Создание графика пользователей: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    # 1. Общее количество задач
    top_users_sorted = top_users.sort_values('total_tasks', ascending=True)
    y_pos = np.arange(len(top_users_sorted))
    ax1.barh(y_pos, top_users_sorted['total_tasks'], color='lightcoral')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top_users_sorted['user'])
    ax1.set_xlabel('Общее количество задач', fontsize=12)
    ax1.set_title(f'Топ {len(top_users)} пользователей по общему количеству задач', fontsize=14)
    ax1.grid(True, alpha=0.3, axis='x')
    # Добавляем значения на бары
    for i, v in enumerate(top_users_sorted['total_tasks']):
        ax1.text(v + 0.1, i, str(int(v)), va='center')
    # 2. Разделение на репортера/исполнителя
    if len(top_users) > 0:
        bottom_users = top_users.head(min(10, len(top_users)))
        x = np.arange(len(bottom_users))
        width = 0.35
        ax2.bar(x - width/2, bottom_users['as_reporter'], width, label='Как репортер', color='lightblue')
        ax2.bar(x + width/2, bottom_users['as_assignee'], width, label='Как исполнитель', color='lightgreen')
        ax2.set_xlabel('Пользователь', fontsize=12)
        ax2.set_ylabel('Количество задач', fontsize=12)
        ax2.set_title(f'Топ {len(bottom_users)} пользователей: репортер vs исполнитель', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(bottom_users['user'], rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"График пользователей сохранен: {output_path}")
# ===== ГРАФИК 4: Задачи по дням =====
def plot_daily_issues_chart(daily_stats: pd.DataFrame, output_path: str):
    """График задач по дням (с накопительным итогом)"""
    if daily_stats.empty:
        print("Нет данных для графика по дням")
        return
    print(f"Создание графика по дням: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    # 1. Ежедневные значения
    dates = pd.to_datetime(daily_stats['date'])
    ax1.plot(dates, daily_stats['created_today'], 'o-', label='Создано', color='green', linewidth=2)
    ax1.plot(dates, daily_stats['resolved_today'], 's-', label='Закрыто', color='red', linewidth=2)
    ax1.fill_between(dates, daily_stats['created_today'], alpha=0.3, color='green')
    ax1.fill_between(dates, daily_stats['resolved_today'], alpha=0.3, color='red')
    ax1.set_title('Количество созданных и закрытых задач по дням', fontsize=14)
    ax1.set_xlabel('Дата', fontsize=12)
    ax1.set_ylabel('Количество задач', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    # 2. Накопительный итог
    ax2.plot(dates, daily_stats['created_cumulative'], '-', label='Создано (накоп.)', color='darkgreen', linewidth=3)
    ax2.plot(dates, daily_stats['resolved_cumulative'], '-', label='Закрыто (накоп.)', color='darkred', linewidth=3)
    ax2.plot(dates, daily_stats['open_cumulative'], '--', label='Открыто (накоп.)', color='orange', linewidth=2)
    ax2.fill_between(dates, daily_stats['created_cumulative'], daily_stats['resolved_cumulative'], 
                     alpha=0.2, color='gray', label='Разница')
    ax2.set_title('Накопительный итог задач', fontsize=14)
    ax2.set_xlabel('Дата', fontsize=12)
    ax2.set_ylabel('Количество задач', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"График по дням сохранен: {output_path}")
# ===== ГРАФИК 5: Затраченное время =====
def plot_time_spent_histogram(time_spent_data: pd.DataFrame, output_path: str):
    """Гистограмма затраченного времени"""
    if time_spent_data.empty:
        print("Нет данных для графика затраченного времени")
        return
    print(f"Создание графика затраченного времени: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(12, 6))
    # Логарифмическая шкала для лучшего отображения
    bins = np.logspace(np.log10(time_spent_data['hours_spent'].min() + 0.1), 
                      np.log10(time_spent_data['hours_spent'].max() + 1), 
                      30)
    plt.hist(time_spent_data['hours_spent'], bins=bins, edgecolor='black', alpha=0.7)
    plt.xscale('log')
    mean_val = time_spent_data['hours_spent'].mean()
    median_val = time_spent_data['hours_spent'].median()
    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                label=f'Среднее: {mean_val:.1f} ч')
    plt.axvline(median_val, color='green', linestyle=':', linewidth=2,
                label=f'Медиана: {median_val:.1f} ч')
    plt.title(f'Распределение затраченного времени (логарифмическая шкала)\nЗадачи с logged time: {len(time_spent_data)}', fontsize=14)
    plt.xlabel('Затраченное время (часы, log scale)', fontsize=12)
    plt.ylabel('Количество задач', fontsize=12)
    plt.grid(True, alpha=0.3, which='both')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"График затраченного времени сохранен: {output_path}")
# ===== ГРАФИК 6: Распределение по состояниям =====
def plot_status_time_distributions(status_data: pd.DataFrame, output_path: str):
    """Распределение времени по состояниям задачи"""
    if status_data.empty:
        print("Нет данных для графика статусов")
        return
    print(f"Создание графика статусов: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    # 1. Box plot по статусам
    status_order = status_data.groupby('status')['hours_in_status'].median().sort_values(ascending=False).index
    sns.boxplot(data=status_data, x='status', y='hours_in_status', order=status_order, ax=ax1)
    ax1.set_title('Время в статусах (Box Plot)', fontsize=14)
    ax1.set_xlabel('Статус', fontsize=12)
    ax1.set_ylabel('Часы в статусе', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    # 2. Количество задач по статусам
    status_counts = status_data['status'].value_counts()
    ax2.bar(range(len(status_counts)), status_counts.values, color='lightblue')
    ax2.set_title('Количество задач по статусам', fontsize=14)
    ax2.set_xlabel('Статус', fontsize=12)
    ax2.set_ylabel('Количество задач', fontsize=12)
    ax2.set_xticks(range(len(status_counts)))
    ax2.set_xticklabels(status_counts.index, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    # Добавляем значения на бары
    for i, v in enumerate(status_counts.values):
        ax2.text(i, v + 0.1, str(v), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"График статусов сохранен: {output_path}")
