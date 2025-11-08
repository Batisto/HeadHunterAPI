import pytest
import json
import os
from src.storage import *
from src.models import *


@pytest.fixture
def test_file(tmp_path):
    file_path = tmp_path / "test_storage.py"
    return str(file_path)


@pytest.fixture
def sample_vacancy():
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000},
        description="We need a junior python developer on board the galley of our startup. At the start, the salary will be like that of a junior, but you will get excellent experience and possibly an option"
    )



def test_init_creates_file(test_file):
    """При инициализации должен создаваться JSON-файл"""
    storage = JSONStorage(test_file)
    assert os.path.exists(storage._filename)
    with open(storage._filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == []


def test_add_vacancy_creates_entry(test_file, sample_vacancy):
    """Добавление вакансии должно сохранять её в JSON"""
    storage = JSONStorage(test_file)
    storage.add_vacancy(sample_vacancy)

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"
    assert "url" in data[0]


def test_get_all_vacancies_returns_objects(test_file, sample_vacancy):
    """get_all_vacancies возвращает список объектов Vacancy"""
    storage = JSONStorage(test_file)
    storage.add_vacancy(sample_vacancy)
    vacancies = storage.get_all_vacancies()

    assert isinstance(vacancies, list)
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"


def test_delete_vacancy_removes_entry(test_file, sample_vacancy):
    """Удаление вакансии должно удалять запись из JSON"""
    storage = JSONStorage(test_file)
    storage.add_vacancy(sample_vacancy)
    storage.delete_vacancy("Python Developer")

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 0
