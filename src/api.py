from abc import abstractmethod, ABC
import requests



class Parser(ABC):
    """Абстрактный метод для работы с API"""

    @abstractmethod
    def load_vacancies(self, keyword: str):
        """Загружает вакансии по ключевому слову"""
        pass

    @abstractmethod
    def get_vacancies(self) -> list:
        """Вернуть список загруженных вакансий"""
    pass


class HeadHunterAPI(Parser):
    def __init__(self):
        self._vacancies: list = []

    def load_vacancies(self, keyword: str, max_pages: int = 5):
        url = "https://api.hh.ru/vacancies"
        all_vacancies = []

        params = {"text": keyword, "page": 0, "per_page": 20}
        response = requests.get(url, params = params)

        if response.status_code != 200:
            self._vacancies = []
            return

        data = response.json()
        total_pages = data.get("pages", 0)
        all_vacancies.extend(data.get("items", []))

        pages_to_load = min(max_pages, total_pages)

        for page in range(1, pages_to_load):
            params["page"] = page
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                all_vacancies.extend(data.get("items", []))
            else:
                break

        self._vacancies = all_vacancies

    def get_vacancies(self) -> list:
        return self._vacancies
