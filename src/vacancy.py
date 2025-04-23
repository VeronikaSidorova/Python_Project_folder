import json
import re
from typing import List, Dict

from src.head_hunter_api import HeadHunterAPI, settings_path


class Vacancy:
    """
    Класс для представления вакансии.
    """
    __slots__ = ('_title', '_url', '_salary_str', '_salary', '_company')

    def __init__(self, title: str, url: str, salary: str, company: str):
        self._title = title
        self._url = url
        self._salary_str = salary  # исходная строка зарплаты
        self._salary = self.parse_salary(salary)  # числовое значение зарплаты
        self._company = company

        # Валидация данных
        self._validate()

    @staticmethod
    def parse_salary(salary_str: str) -> float:
        """
        Парсит строку с зарплатой и возвращает числовое значение (float).
        Если указан диапазон или слова "от", "до" — берется минимальное число.
        Если не удалось распарсить — возвращается 0.
        """
        if not isinstance(salary_str, str):
            raise ValueError("Зарплата должна быть строкой.")

        # Удаляем пробелы и приводим к нижнему регистру
        s = salary_str.lower().replace(' ', '')

        # Ищем все числа (целые или с десятичной точкой)
        numbers = re.findall(r'\d+\.?\d*', s)

        if not numbers:
            return 0.0

        # Преобразуем найденные числа в float
        nums = [float(num) for num in numbers]

        # Логика выбора значения:
        # Если есть слова "от" — берем минимальное число
        if 'от' in s:
            return min(nums)

        # Если есть слова "до" — берем максимальное число
        if 'до' in s:
            return max(nums)

        # Если просто диапазон через дефис или тире (например "100000-150000")
        if '-' in s or '–' in s:
            return min(nums)

        # Иначе берем первое число как зарплату
        return nums[0]

    def _validate(self):
        """Метод для валидации данных вакансии."""
        if not isinstance(self._title, str) or not self._title.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")

        # if not isinstance(self._url, str) or not self._url.startswith("https"):
        #     raise ValueError("Ссылка на вакансию должна быть корректным URL.")

        if not isinstance(self._salary, (int, float)) or self._salary < 0:
            raise ValueError(f"Зарплата должна быть неотрицательным числом. Получено: {self._salary}")

        if not isinstance(self._company, str):
            raise ValueError("Компания должна быть строкой.")

    @classmethod
    def cast_to_object_list(cls, vacancies_data) -> List:
        """Преобразует список словарей вакансий в список объектов Vacancy."""
        vacancies_objects = []

        for vacancy in vacancies_data:
            try:
                # Предполагаем, что структура данных соответствует ожиданиям
                title = vacancy['name']
                url = vacancy['alternate_url']
                salary = vacancy['salary']
                company = vacancy['employer']['name']


                # Создаем объект Vacancy и добавляем его в список
                vacancies_objects.append(Vacancy(title, salary, company, url))
            except KeyError as e:
                print(f"Ошибка при обработке вакансии: отсутствует ключ {e}")
            except ValueError as e:
                print(f"Ошибка валидации данных вакансии: {e}")

        return vacancies_objects


    def __lt__(self, other):
        """Сравнение вакансий по зарплате (меньше)."""
        return self._salary < other.salary

    def __le__(self, other):
        """Сравнение вакансий по зарплате (меньше или равно)."""
        return self._salary <= other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зарплате (равно)."""
        return self._salary == other.salary

    def __gt__(self, other):
        """Сравнение вакансий по зарплате (больше)."""
        return self._salary > other.salary

    def __ge__(self, other):
        """Сравнение вакансий по зарплате (больше или равно)."""
        return self._salary >= other.salary

    def __str__(self):
        """Строковое представление вакансии."""
        return (f"Вакансия: {self._title}, Зарплата: {self._salary} ({self._salary_str}), "
                f"Ссылка: {self._url}, Компания: {self._company}")

hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

print(vacancies_list)