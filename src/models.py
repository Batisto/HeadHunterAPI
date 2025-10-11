class Vacancy:
    """
    Класс, представляющий вакансию.
    Содержит основные данные по вакансии и методы сравнения по зарплате
    """

    def __init__(self, title: str, url: str, salary: int | float | None, description: str):
        self._title = title
        self._url = url
        self._salary = salary
        self._description = description

    @property
    def title(self) -> str:
        return self._title


    @property
    def salary(self):
        return self._salary

    def __eq__(self, other) -> bool:
        """Проверяет равенство вакансий по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary == other._salary


    def __lt__(self, other) -> bool:
        """Проверяет, что зарплата этой вакансии, больше, чем другой"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary > other._salary
