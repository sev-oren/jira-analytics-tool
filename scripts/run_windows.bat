@echo off
echo ========================================
echo JIRA Analytics Tool - Windows Launcher
echo ========================================
echo.
REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python не установлен или не добавлен в PATH!
    echo Установите Python 3.8 или выше с сайта python.org
    pause
    exit /b 1
)
REM Проверка виртуального окружения
if not exist "venv" (
    echo WARNING: Виртуальное окружение не найдено.
    echo Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
)
REM Активация виртуального окружения
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Не удалось активировать виртуальное окружение
    pause
    exit /b 1
)
REM Установка/обновление зависимостей
echo.
echo Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt
REM Создание необходимых папок
if not exist "logs" mkdir logs
if not exist "plots" mkdir plots
if not exist "config" mkdir config
REM Проверка конфигурации
if not exist "config\config.yaml" (
    echo WARNING: Конфигурационный файл не найден.
    echo Будет использована конфигурация по умолчанию.
)
REM Запуск приложения
echo.
echo ========================================
echo Запуск JIRA Analytics Tool...
echo ========================================
echo.
python src\main.py
REM Пауза для просмотра результатов
echo.
echo ========================================
echo Выполнение завершено.
echo Проверьте папку plots/ для просмотра графиков.
echo ========================================
pause
