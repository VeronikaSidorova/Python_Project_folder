import requests

from src.job_api import JobAPI


class HeadHunterAPI(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def connect(self):
        """Проверка подключения к API"""
        try:
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()  # Проверка на ошибки
            return True
        except requests.RequestException as e:
            print(f"Ошибка подключения к API: {e}")
            return False

    def get_vacancies(self, query: str, area: str = None):
        """Получение вакансий по запросу"""
        params = {'text': query}
        if area:
            params['area'] = area

        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Проверка на ошибки
            return response.json().get('items', [])
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []



hh = HeadHunterAPI().get_vacancies("Python")
print(hh)