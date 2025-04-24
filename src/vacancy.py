import re
from typing import List


class Vacancy:
    """
    Класс для представления вакансии.
    """

    __slots__ = ("_title", "_url", "_salary_str", "_salary", "_company")

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
        s = salary_str.lower().replace(" ", "")

        # Ищем все числа (целые или с десятичной точкой)
        numbers = re.findall(r"\d+\.?\d*", s)

        if not numbers:
            return 0.0

        # Преобразуем найденные числа в float
        nums = [float(num) for num in numbers]

        # Логика выбора значения:
        # Если есть слова "от" — берем минимальное число
        if "от" in s:
            return min(nums)

        # Если есть слова "до" — берем максимальное число
        if "до" in s:
            return max(nums)

        # Если просто диапазон через дефис или тире (например "100000-150000")
        if "-" in s or "–" in s:
            return min(nums)

        # Иначе берем первое число как зарплату
        return nums[0]

    def _validate(self) -> None:
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
    def cast_to_object_list(cls, vacancies_data: List) -> List:
        """Преобразует список словарей вакансий в список объектов Vacancy."""
        vacancies_objects = []

        for vacancy in vacancies_data:
            try:
                # Предполагаем, что структура данных соответствует ожиданиям
                title = vacancy["name"]
                url = vacancy["alternate_url"]
                salary = vacancy["salary"]
                company = vacancy["employer"]["name"]
                # Формируем строку зарплаты
                salary_str = ""
                if isinstance(salary, dict):
                    from_salary = salary.get("from")
                    to_salary = salary.get("to")
                    if from_salary is not None and to_salary is not None:
                        salary_str = f"{from_salary} - {to_salary} {salary['currency']}"
                    elif from_salary is not None:
                        salary_str = f"от {from_salary} {salary['currency']}"
                    elif to_salary is not None:
                        salary_str = f"до {to_salary} {salary['currency']}"
                    else:
                        salary_str = "не указана"
                else:
                    salary_str = str(salary)  # Если зарплата уже строка

                # Создаем объект Vacancy и добавляем его в список
                vacancies_objects.append(Vacancy(title, url, salary_str, company))
            except KeyError as e:
                print(f"Ошибка при обработке вакансии: отсутствует ключ {e}")
            except ValueError as e:
                print(f"Ошибка валидации данных вакансии: {e}")

        return vacancies_objects

    def to_dict(self): # type: ignore
        """Метод для преобразования объекта Vacancy в словарь."""
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __lt__(self, other): # type: ignore
        """Сравнение вакансий по зарплате (меньше)."""
        return self._salary < other.salary

    def __le__(self, other): # type: ignore
        """Сравнение вакансий по зарплате (меньше или равно)."""
        return self._salary <= other.salary

    def __eq__(self, other): # type: ignore
        """Сравнение вакансий по зарплате (равно)."""
        return self._salary == other.salary

    def __gt__(self, other): # type: ignore
        """Сравнение вакансий по зарплате (больше)."""
        return self._salary > other.salary

    def __ge__(self, other): # type: ignore
        """Сравнение вакансий по зарплате (больше или равно)."""
        return self._salary >= other.salary

    def __str__(self): # type: ignore
        """Строковое представление вакансии."""
        return (
            f"Вакансия: {self._title}, Зарплата: {self._salary} ({self._salary_str}), "
            f"Ссылка: {self._url}, Компания: {self._company}"
        )

    @property
    def url(self): # type: ignore
        return self._url

    @property
    def title(self): # type: ignore
        return self._title
