import json
import os
from abc import ABC, abstractmethod
from typing import List
from src.models import Vacancy


class VacancyStorage(ABC):
    """Абстрактный метод для хранения вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """Добавить вакансию в хранилище"""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Vacancy]:
        """"Получить все вакансии"""
        pass

    @abstractmethod
    def delete_vacancy(self, title: str):
        """Удалить вакансию по названию"""
        pass

class JSONStorage(VacancyStorage, ABC):
    """Хранилище вакансий в JSON-файле"""

    def __init__(self, filename: str = "vacancies.json"):
        # получаем путь к текущему файлу (storage.py)
        base_dir = os.path.dirname(__file__)
        # поднимаемся на уровень выше, чтобы попасть в корень проекта
        project_root = os.path.dirname(base_dir)
        # формируем путь до data
        self._filename = os.path.join(project_root, "data", filename)

        # создаем папку, если её нет
        folder = os.path.dirname(self._filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # создаем файл, если его нет
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        """Добавляет новую вакансию в JSON-файл"""
        try:
            #Загружаем существующие данные из файла
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        #Преобразуем объект Vacancy в словарь
        vacancy_dict = vacancy.to_dict()

        #Проверяем нет ли уже вакансий с таким же url
        for existing_vacancy in data:
            if existing_vacancy.get('url') == vacancy_dict.get('url'):
                print("Ошибка! Вакансия с таким url уже существует.")
                return False

        #Проверяем нет ли уже вакансии с таким же title. Если есть, то присваиваем индекс
        base_title = vacancy_dict['title']
        same_titles = [v for v in data if v.get('title', '').startswith(base_title)]

        if same_titles:
            new_title = f"{base_title} ({len(same_titles)})"
            vacancy_dict['title'] = new_title
        else:
            new_title = base_title

        #Добавляем новую вакансию в список
        data.append(vacancy_dict)

        #Перезаписываем JSON-файл с обновленными данными
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'Вакансия {new_title} была успешно добавлена')

    def get_all_vacancies(self) -> List[Vacancy]:
        """Возвращает список всех вакансий из JSON-файла"""
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        vacancies = []

        for item in data:
            vacancy = Vacancy(
                title = item.get('title'),
                url = item.get('url'),
                salary = item.get('salary'),
                description = item.get('description')
            )

            vacancies.append(vacancy)

        return vacancies

    def delete_vacancy(self, title: str):
        """Удаляет вакансию по названию"""
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Файл с вакансиями не найден")
            return False

        new_data = [v for v in data if v.get('title') != title]

        if len(new_data) == len(data):
            print(f"Вакансия с названием {title} не найдена")
            return False

        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        print(f"Вакансия {title} была удалена")
        return True
