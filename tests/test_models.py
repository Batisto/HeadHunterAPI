import pytest
from src.models import *


@pytest.fixture
def vacancy_data():
    return {
        "title": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "description": "We need a junior python developer on board the galley of our startup. At the start, the salary will be like that of a junior, but you will get excellent experience and possibly an option"
    }


def test_vacancy_initialization(vacancy_data):
    """Проверяем инициализацию полей"""
    v = Vacancy(**vacancy_data)

    assert v.title == "Python Developer"
    assert v._url == "https://hh.ru/vacancy/123"
    assert v.salary == 125000
    assert v._description == "We need a junior python developer on board the galley of our startup. At the start, the salary will be like that of a junior, but you will get excellent experience and possibly an option"


def test_vacancy_salary_one(vacancy_data):
    """Проверяем логику работы, когда salary: None"""
    v = Vacancy("QA Engineer", "https://hh.ru/vacancy/456", None, "Тестирование")

    assert v.salary == 0


def test_vacancy_salary_only_from():
    """Если указан только from"""
    v = Vacancy("DevOps", "https://hh.ru/vacancy/789", {"from": 80000}, "CI/CD")
    assert v.salary == 80000


def test_vacancy_salary_only_to():
    """Если указан только to"""
    v = Vacancy("Frontend", "https://hh.ru/vacancy/999", {"to": 120000}, "React")
    assert v.salary == 120000


def test_vacancy_comparison():
    """Проверяем сравнение по зарплате"""
    v1 = Vacancy("Junior", "url1", {"from": 50000, "to": 60000}, "desc")
    v2 = Vacancy("Middle", "url2", {"from": 100000, "to": 120000}, "desc")
    assert v1 < v2
    assert not v2 < v1
    assert v1 != v2


def test_vacancy_to_dict(vacancy_data):
    """Проверяем преобразование в словарь"""
    v = Vacancy(**vacancy_data)
    result = v.to_dict()
    assert isinstance(result, dict)
    assert result["title"] == "Python Developer"
    assert "url" in result
    assert "salary" in result
    assert "description" in result
