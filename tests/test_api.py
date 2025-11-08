import pytest
import requests
from src.api import *


@pytest.fixture
def mock_response(monkeypatch):
    """Подделывает ответ requests.get"""
    def fake_get(url, params):
        class FakeResponse:
            status_code = 200
            def json(self):
                return {
                    "pages": 2,
                    "items": [
                        {"name": "Python Developer", "alternate_url": "https://hh.ru/vac/1", "salary": {"from": 100000, "to": 150000}},
                        {"name": "QA Engineer", "alternate_url": "https://hh.ru/vac/2", "salary": {"from": 80000, "to": 100000}}
                    ]
                }
        return FakeResponse()
    monkeypatch.setattr(requests, "get", fake_get)


def test_load_vacancies_success(mock_response):
    """Проверяем, что load_vacancies корректно загружает и сохраняет вакансии"""
    api = HeadHunterAPI()
    api.load_vacancies("Python", max_pages=1)

    vacancies = api.get_vacancies()
    assert isinstance(vacancies, list)
    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["salary"]["from"] == 80000


def test_load_vacancies_failed(monkeypatch):
    """Если сервер возвращает не 200, вакансии должны быть пустыми"""
    def fake_get(url, params):
        class FakeResponse:
            status_code = 500
            def json(self):
                return {}
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    api = HeadHunterAPI()
    api.load_vacancies("Python")
    assert api.get_vacancies() == []
