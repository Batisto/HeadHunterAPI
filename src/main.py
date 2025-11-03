from src.api import HeadHunterAPI
from src.storage import JSONStorage
from src.models import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()

    # Читаем из старого файла (источник)
    source_storage = JSONStorage("vacancies.json")

    # Записываем новые данные сюда
    target_storage = JSONStorage("hh_vacancies.json")

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

        #Поиск вакансий и запись в hh_vacancies.json

        if choice == "1":
            keyword = input("Введите ключевое слово: ")

            hh_api.load_vacancies(keyword)
            vacancies_data = hh_api.get_vacancies()

            print(f"DEBUG: Загружено вакансий — {len(vacancies_data)}")

            if not vacancies_data:
                print("Ничего не найдено")
                continue

            count = 0
            for item in vacancies_data:
                vacancy = Vacancy(
                    title=item.get("name"),
                    url=item.get("alternate_url"),
                    salary=item.get("salary"),
                    description=item.get("snippet", {}).get("responsibility", "Описание отсутствует")
                )

                if target_storage.add_vacancy(vacancy) is not False:
                    count += 1

            print(f"Добавлено вакансий: {count}")

        # Показать все сохранённые вакансии

        elif choice == "2":
            vacancies = source_storage.get_all_vacancies()

            if not vacancies:
                print("Вакансии отсутствуют.")
                continue

            print("\n=== Сохранённые вакансии ===")
            for v in vacancies:
                print(f"- {v.title} ({v.salary} руб.) — {v._url}")
            print("=============================\n")

        # Топ N вакансий по зарплате
        elif choice == "3":
            try:
                n = int(input("Сколько топ-вакансий необходимо вывести?\n"))
            except ValueError:
                print("Ошибка, нужно ввести число")
                continue

            vacancies = target_storage.get_all_vacancies()
            vacancies_with_salary = []

            for v in vacancies:
                if v.salary:
                    if isinstance(v.salary, dict):
                        salary_value = v.salary.get("to") or v.salary.get("from")
                    else:
                        salary_value = v.salary
                    if salary_value:
                        vacancies_with_salary.append((salary_value, v))

            vacancies_with_salary.sort(key=lambda x: x[0], reverse=True)

            print(f"\nТоп {n} вакансий по зарплате:\n")
            for salary, v in vacancies_with_salary[:n]:
                print(f"{v.title} — {salary} руб.")
                print(f"Ссылка: {v._url}")
                print(f"Описание: {v._description[:120]}...\n")

        # Удаление вакансии

        elif choice == "4":
            title = input("Введите название вакансии для удаления: ")
            target_storage.delete_vacancy(title)

        # Выход
        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Ошибка! Введите цифру от 1 до 5.")


if __name__ == "__main__":
    user_interaction()
