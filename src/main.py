from src.api import HeadHunterAPI
from src.storage import JSONStorage
from src.models import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    while True:
        print("""
Выберите действие:
1 — Найти вакансии по ключевому слову
2 — Показать все сохранённые вакансии
3 — Показать топ N вакансий по зарплате
4 — Удалить вакансию по названию
5 — Выход
""")

        choice = input("Ваш выбор: ")

        if choice == "1":
            keyword = input("Введите ключевое слово: ")

            hh_api.load_vacancies(keyword)
            vacancies_data = hh_api.get_vacancies()

            if not vacancies_data:
                print("Ничего не найдено")
                continue

            count = 0
            for item in vacancies_data:
                vacancy = Vacancy(
                    title = item.get("name"),
                    url = item.get("alternate_url"),
                    salary = item.get("salary"),
                    description = item.get("snippet", {}).get("responsibility", "Описание отсутствует")
                )

                if storage.add_vacancy(vacancy) is not False:
                    count += 1

            print(f'Добавлено вакансий: {count}')

        elif choice == "2":
            print("Список вакансий… (пока без реализации)")
        elif choice == "3":
            print("Топ вакансий… (пока без реализации)")
        elif choice == "4":
            print("Удаление… (пока без реализации)")
        elif choice == "5":
            print("Выход из программы")
            break
        else:
            print("Ошибка! Введите цифру от 1 до 5.")


if __name__ == "__main__":
    user_interaction()
