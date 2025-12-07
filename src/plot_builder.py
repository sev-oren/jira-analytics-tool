import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np
def plot_open_time_histogram(df: pd.DataFrame, output_path: str):
    """
    Построить гистограмму времени в открытом состоянии
    Args:
        df: DataFrame с колонками ['key', 'open_hours']
        output_path: Путь для сохранения графика
    """
    if df.empty:
        print(" Нет данных для построения графика")
        return
    print(f" Создание гистограммы...")
    print(f"   Данных: {len(df)} точек")
    print(f"   Сохранение в: {output_path}")
    # Создаем папку если нет
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Создаем фигуру
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
    # 2. Box plot (ящик с усами)
    sns.boxplot(data=df, y='open_hours', ax=ax2)
    ax2.set_title('Распределение времени (Box Plot)', fontsize=14)
    ax2.set_ylabel('Часы в открытом состоянии', fontsize=12)
    ax2.grid(True, alpha=0.3)
    # Добавляем аннотации
    stats_text = f'''
    Статистика:
    • Min: {df["open_hours"].min():.1f} ч
    • 25%: {df["open_hours"].quantile(0.25):.1f} ч  
    • 50%: {df["open_hours"].median():.1f} ч
    • 75%: {df["open_hours"].quantile(0.75):.1f} ч
    • Max: {df["open_hours"].max():.1f} ч
    • Mean: {df["open_hours"].mean():.1f} ч
    • Std: {df["open_hours"].std():.1f} ч
    '''
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes,
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    # Сохраняем
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f" Гистограмма сохранена: {output_path}")
    # Показываем путь к файлу
    if os.path.exists(output_path):
        size_kb = os.path.getsize(output_path) / 1024
        print(f"   Размер файла: {size_kb:.1f} KB")
# Другие функции графиков (заглушки)
def plot_status_time_distributions(status_data: pd.DataFrame, output_path: str):
    """Построить распределение времени по состояниям"""
    print(" Функция plot_status_time_distributions еще не реализована")
    pass
def plot_daily_issues_chart(daily_stats: pd.DataFrame, output_path: str):
    """График задач по дням"""
    print(" Функция plot_daily_issues_chart еще не реализована")
    pass
def plot_top_users_chart(top_users: pd.DataFrame, output_path: str):
    """График топ пользователей"""
    print(" Функция plot_top_users_chart еще не реализована")
    pass
def plot_time_spent_histogram(time_spent_data: pd.DataFrame, output_path: str):
    """Гистограмма затраченного времени"""
    print(" Функция plot_time_spent_histogram еще не реализована")
    pass
def plot_priority_distribution_chart(priority_data: pd.DataFrame, output_path: str):
    """Распределение задач по приоритетам"""
    print(" Функция plot_priority_distribution_chart еще не реализована")
    pass

