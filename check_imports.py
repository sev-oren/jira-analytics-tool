#!/usr/bin/env python3
"""Проверка импортов проекта"""
import sys
import os
print("=" * 60)
print("ПРОВЕРКА ИМПОРТОВ ПРОЕКТА")
print("=" * 60)
print(f"\n1. Python информация:")
print(f"   Версия: {sys.version}")
print(f"   Исполняемый файл: {sys.executable}")
print(f"   Текущая папка: {os.getcwd()}")
print(f"\n2. Содержимое папки:")
for item in os.listdir('.'):
    print(f"   {item}")
print("\n3. Проверка библиотек:")
try:
    import requests
    print("   ✓ requests")
except:
    print("   ✗ requests")
try:
    import pandas as pd
    print(f"   ✓ pandas ({pd.__version__})")
except:
    print("   ✗ pandas")
try:
    import matplotlib
    print(f"   ✓ matplotlib ({matplotlib.__version__})")
except:
    print("   ✗ matplotlib")
try:
    import seaborn
    print(f"   ✓ seaborn ({seaborn.__version__})")
except:
    print("   ✗ seaborn")
try:
    import yaml
    print("   ✓ PyYAML")
except:
    print("   ✗ PyYAML")
print("\n" + "=" * 60)
print("Проверка завершена!")
