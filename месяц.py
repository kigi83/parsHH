import requests
from datetime import datetime, timedelta

AREA = 1  # Код региона (Москва)
PERIOD = 30  # Период до сегодняшнего дня за который опубликована вакансия

def get_vacancies_hh(language):
    url = 'https://api.hh.ru/vacancies'
    per_page = 100  # Количество вакансий на одной странице
    vacancies_processed = 0

    today = datetime.now().date()
    period_start = today - timedelta(days=PERIOD)

    page = 0
    while True:
        params = {
            'text': language,
            'area': AREA,
            'date_from': period_start.isoformat(),  # Устанавливаем начальную дату периода
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        page_payload = response.json()

        for i in range(len(page_payload["items"])):
            vacancy = page_payload["items"][i]
            print(f"Информация о вакансии {i + 1}:")
            print("Название вакансии:", vacancy["name"])
            print("URL вакансии:", vacancy["alternate_url"])

            if "employer" in vacancy and "url" in vacancy["employer"]:
                url_employer = vacancy["employer"]["url"]
                print("Выполняется запрос к сайту работодателя...")
                response_employer = requests.get(url_employer)
                response_employer.raise_for_status()
                print("Запрос к сайту работодателя выполнен успешно.")

                employer_info = response_employer.json()
                print("Название компании:", employer_info["name"])
                print("URL сайта компании:", employer_info["site_url"])
            else:
                print("Информация о работодателе отсутствует.")

            print("---")

            vacancies_processed += 1

        if page_payload["page"] < page_payload["pages"] - 1:
            page += 1
        else:
            break

    print(f"Обработано всего вакансий: {vacancies_processed}")

get_vacancies_hh("Водитель")
