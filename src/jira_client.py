import requests
import logging
from typing import List, Dict, Optional
logger = logging.getLogger(__name__)
class JiraClient:
    """Клиент для работы с JIRA REST API"""
    def __init__(self, server_url: str, project_key: str, max_results: int = 100):
        """
        Инициализация клиента JIRA
        Args:
            server_url: URL сервера JIRA
            project_key: Ключ проекта (например, 'KAFKA')
            max_results: Максимальное количество результатов
        """
        self.server_url = server_url.rstrip('/')
        self.project_key = project_key
        self.max_results = max_results
        self.session = requests.Session()
        # Настройка сессии
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    def get_issues(self, jql: str) -> List[Dict]:
        """
        Получить задачи по JQL запросу
        Args:
            jql: JQL запрос
        Returns:
            Список задач
        """
        url = f"{self.server_url}/rest/api/2/search"
        params = {
            'jql': jql,
            'maxResults': self.max_results,
            'fields': 'key,created,resolutiondate,status,assignee,reporter,priority,timespent,worklog,issuetype,summary'
        }
        try:
            print(f"🔗 Запрос к JIRA: {url}")
            print(f"🔍 JQL: {jql}")
            print(f"📊 Макс. результатов: {self.max_results}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            issues = data.get('issues', [])
            print(f"📥 Получено задач: {len(issues)}")
            # Логируем первую задачу для отладки
            if issues:
                first_issue = issues[0]
                print(f"📋 Пример задачи: {first_issue['key']} - {first_issue['fields']['summary'][:50]}...")
            return issues
        except requests.exceptions.ConnectionError:
            print("❌ Ошибка соединения. Проверьте интернет-подключение.")
            return []
        except requests.exceptions.Timeout:
            print("❌ Таймаут запроса. Сервер не отвечает.")
            return []
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP ошибка: {e}")
            print(f"   URL: {url}")
            print(f"   Параметры: {params}")
            return []
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return []
    def test_connection(self) -> bool:
        """Проверка соединения с JIRA"""
        try:
            url = f"{self.server_url}/rest/api/2/serverInfo"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            print(f"✅ Соединение с JIRA установлено: {self.server_url}")
            return True
        except Exception as e:
            print(f"❌ Не удалось подключиться к JIRA: {e}")
            return False
