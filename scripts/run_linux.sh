#!/bin/bash
# JIRA Analytics Tool - Linux Launcher
echo "========================================"
echo "JIRA Analytics Tool - Linux Launcher"
echo "========================================"
echo
# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 не установлен!"
    echo "Установите: sudo apt-get install python3 python3-pip"
    exit 1
fi
# Проверка версии Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
REQUIRED_VERSION="3.8.0"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "WARNING: Требуется Python 3.8 или выше, текущая версия: $PYTHON_VERSION"
fi
# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "WARNING: Виртуальное окружение не найдено."
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Не удалось создать виртуальное окружение"
        exit 1
    fi
fi
# Активация виртуального окружения
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Не удалось активировать виртуальное окружение"
    exit 1
fi
# Установка/обновление зависимостей
echo
echo "Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt
# Создание необходимых папок
mkdir -p logs plots config
# Проверка конфигурации
if [ ! -f "config/config.yaml" ]; then
    echo "WARNING: Конфигурационный файл не найден."
    echo "Будет использована конфигурация по умолчанию."
fi
# Запуск приложения
echo
echo "========================================"
echo "Запуск JIRA Analytics Tool..."
echo "========================================"
echo
python3 src/main.py
# Итог
echo
echo "========================================"
echo "Выполнение завершено."
echo "Проверьте папку plots/ для просмотра графиков."
echo "========================================"
