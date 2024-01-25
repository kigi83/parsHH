from datetime import datetime, timedelta
import requests
import re

AREA = 1  # Код региона (Москва)
PERIOD = 2  # Период до сегодняшнего дня, за который опубликована вакансия
PER_PAGE = 20  # Количество вакансий на одной странице


def get_employer_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        employer_info = response.json()
        return {
            "Компания": employer_info["name"],
            "Сайт": employer_info.get("site_url", "")
        }
    else:
        return None


def get_vacancies_hh(keyword):
    url = 'https://api.hh.ru/vacancies'
    vacancies_info = []

    today = datetime.now().date()
    period_start = today - timedelta(days=PERIOD)

    page = 0
    while True:
        params = {
            'text': keyword,
            'area': AREA,
            'date_from': period_start.isoformat(),
            'per_page': PER_PAGE,
            'page': page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        page_payload = response.json()
        print(f"Processing page {page}, total pages: {page_payload['pages']}")

        for vacancy in page_payload["items"]:
            if "employer" in vacancy and "url" in vacancy["employer"]:
                url_employer = vacancy["employer"]["url"]
                company_data = get_employer_info(url_employer)
                if company_data:
                    vacancies_info.append(company_data)

        if page < page_payload["pages"] - 1:
            page += 1
        else:
            break

    return vacancies_info


result = get_vacancies_hh("консьерж")
print(result)


def filter_and_create_dict(vacancies):
    filtered_companies = [company for company in vacancies if company.get('Сайт') != '']
    company_final = {}
    for company in filtered_companies:
        try:
            response = requests.get(company['Сайт'])
            response.raise_for_status()
            string = response.text
            pattern = '"tel:(.*?)"'
            match = re.search(pattern, string)
            if match is not None:
                company_final[company['Компания']] = {
                    'Сайт': company['Сайт'],
                    'Телефон': match.group(1)
                }
        except requests.RequestException as error:
            pass
    return company_final


vacancies_data = get_vacancies_hh("консьерж")
result = filter_and_create_dict(vacancies_data)
print(result)
