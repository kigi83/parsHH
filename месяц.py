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

        for vacancy in page_payload["items"]:
            print("Название вакансии:", vacancy["name"])
            print("URL вакансии:", vacancy["alternate_url"])
            # Другая обработка данных о вакансиях

            vacancies_processed += 1

        if page_payload["pages"] > page + 1:
            page += 1
        else:
            break

    print(f"Обработано всего вакансий: {vacancies_processed}")

get_vacancies_hh("Водитель")
