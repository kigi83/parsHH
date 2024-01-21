import requests
from datetime import datetime, timedelta

AREA = 1  # Код региона (Москва)
PERIOD = 30  # Период до сегодняшнего дня за который опубликована вакансия


def get_vacancies_hh(language):
    url = 'https://api.hh.ru/vacancies'
    per_page = 100  # Количество вакансий на одной странице
    vacancies_info = []

    today = datetime.now().date()
    period_start = today - timedelta(days=PERIOD)

    page = 0
    while True:
        params = {
            'text': language,
            'area': AREA,
            'date_from': period_start.isoformat(),
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        page_payload = response.json()

        for vacancy in page_payload["items"]:
            if "employer" in vacancy and "url" in vacancy["employer"]:
                url_employer = vacancy["employer"]["url"]
                response_employer = requests.get(url_employer)
                if response_employer.status_code == 200:
                    employer_info = response_employer.json()
                    company_data = {
                        "Компания": employer_info["name"],
                        "Сайт": employer_info.get("site_url", "Информация отсутствует")
                    }
                    vacancies_info.append(company_data)

        if page_payload["page"] < page_payload["pages"] - 1:
            page += 1
        else:
            break

    return vacancies_info


get_vacancies_hh("Водитель")
