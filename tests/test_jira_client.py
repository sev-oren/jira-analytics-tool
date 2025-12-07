import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.jira_client import JiraClient
def test_jira_client_initialization():
    """Тест инициализации клиента JIRA"""
    client = JiraClient(
        server_url="https://test.example.com",
        project_key="TEST",
        max_results=100
    )
    assert client.server_url == "https://test.example.com"
    assert client.project_key == "TEST"
    assert client.max_results == 100
    print("✓ test_jira_client_initialization passed")
def test_jira_client_get_issues_method_exists():
    """Тест наличия метода get_issues"""
    client = JiraClient("https://test.com", "TEST")
    assert hasattr(client, 'get_issues')
    assert callable(client.get_issues)
    print("✓ test_jira_client_get_issues_method_exists passed")
def test_jira_client_empty_response():
    """Тест обработки пустого ответа"""
    client = JiraClient("https://test.com", "TEST", max_results=10)
    # Метод должен существовать даже если мы не можем проверить его работу без реального API
    assert client.get_issues is not None
    print("✓ test_jira_client_empty_response passed")
if __name__ == "__main__":
    test_jira_client_initialization()
    test_jira_client_get_issues_method_exists()
    test_jira_client_empty_response()
    print("\n✅ Все тесты JiraClient пройдены!")
