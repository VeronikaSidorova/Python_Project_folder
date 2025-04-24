import json
from pathlib import Path

import requests

from src.job_api import JobAPI

settings_path = Path(__file__).parent.parent / "data" / "vacancy.json"

class HeadHunterAPI(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__session = requests.Session()
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []

    def _connect(self):
        """Проверка подключения к API"""
        try:
            response = self.__session.get(self.BASE_URL)
            response.raise_for_status()  # Проверка на ошибки
            return True
        except requests.RequestException as e:
            print(f"Ошибка подключения к API: {e}")
            return False

    def get_vacancies(self, query: str):
        """Получение вакансий по запросу"""
        params = {'text': query,
                  'per_page': 20}
        # if area:
        #     params['area'] = area

        try:
            response = self.__session.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Проверка на ошибки
            result = response.json().get('items', [])
            return result
        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
        
