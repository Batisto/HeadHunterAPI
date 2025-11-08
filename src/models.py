class Vacancy:
    """
    Класс, представляющий вакансию.
    Содержит основные данные по вакансии и методы сравнения по зарплате
    """

    def __init__(self, title: str, url: str, salary: int | float | None | dict, description: str):
        self._title = title
        self._url = url
        self._salary = salary
        self._description = description

    @property
    def title(self) -> str:
        return self._title


    @property
    def salary(self):
        if self._salary is None:
            return 0
        if isinstance(self._salary, dict):
            from_val = self._salary.get("from")
            to_val = self._salary.get("to")
            if from_val is not None and to_val is not None:
                return int((from_val + to_val) / 2)
            if from_val is None:
                return int(to_val)
            if to_val is None:
                return int(from_val)
            else:
                return 0
        else:
            return int(self._salary)

    def __eq__(self, other) -> bool:
        """Проверяет равенство вакансий по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary


    def __lt__(self, other) -> bool:
        """Проверяет, что зарплата этой вакансии, меньше, чем другой"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def to_dict(self) -> dict:
        """Преобразует объект Vacancy в словарь для хранения в JSON"""
        return {
            "title": self._title,
            "url": self._url,
            "salary": self.salary,
            "description": self._description
        }

    @classmethod
    def from_api_to_dict(cls, data: dict) -> "Vacancy":
        """Создает Vacancy из одного элемента items"""
        title = data.get("title", "")
        url = data.get("url")
        salary_raw = data.get("salary")
        snippet = data.get("snippet", {})
        requirement = snippet.get("requirement")
        responsibility = snippet.get("responsibility")
        description = ' '.join(filter(None, [requirement, responsibility]))

        return cls(title, url, salary_raw, description)
