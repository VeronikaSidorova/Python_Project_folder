import re
from typing import List, Dict


class Vacancy:
    """
    Класс для представления вакансии.
    """

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary_str = salary  # исходная строка зарплаты
        self.salary = self.parse_salary(salary)  # числовое значение зарплаты
        self.description = description

        # Валидация данных
        self.validate()

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

    def validate(self):
        """Метод для валидации данных вакансии."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")

        if not isinstance(self.url, str) or not self.url.startswith("http"):
            raise ValueError("Ссылка на вакансию должна быть корректным URL.")

        if not isinstance(self.salary, (int, float)) or self.salary < 0:
            raise ValueError(f"Зарплата должна быть неотрицательным числом. Получено: {self.salary}")

        if not isinstance(self.description, str):
            raise ValueError("Описание должно быть строкой.")

    @classmethod
    def cast_to_object_list(cls, data_list: List[Dict]) -> List['Vacancy']:
        vacancies_list = []

        for data in data_list:
            try:
                vacancy = cls(
                    title=data['title'],
                    url=data['url'],
                    salary=data['salary'],
                    description=data['description']
                )
                vacancies_list.append(vacancy)
            except KeyError as e:
                raise ValueError(f"Отсутствует обязательный ключ: {e}")
            except Exception as e:
                raise ValueError(f"Ошибка при создании вакансии: {e}")

        return vacancies_list


    def __lt__(self, other):
        """Сравнение вакансий по зарплате (меньше)."""
        return self.salary < other.salary

    def __le__(self, other):
        """Сравнение вакансий по зарплате (меньше или равно)."""
        return self.salary <= other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зарплате (равно)."""
        return self.salary == other.salary

    def __gt__(self, other):
        """Сравнение вакансий по зарплате (больше)."""
        return self.salary > other.salary

    def __ge__(self, other):
        """Сравнение вакансий по зарплате (больше или равно)."""
        return self.salary >= other.salary

    def __str__(self):
        """Строковое представление вакансии."""
        return f"Вакансия: {self.title}, Зарплата: {self.salary} ({self.salary_str}), Ссылка: {self.url}, Описание: {self.description}"


# Пример использования:
vacancy1 = Vacancy("Python Developer", "https://example.com/vacancy1", "от 120000", "Разработка приложений на Python.")
vacancy2 = Vacancy("Java Developer", "https://example.com/vacancy2", "100 000 - 150 000",
                   "Разработка приложений на Java.")
vacancy3 = Vacancy("Frontend Developer", "https://example.com/vacancy3", "до 90000", "Разработка интерфейсов.")

print(vacancy1)
print(vacancy2)
print(vacancy3)

# Сравнение вакансий по зарплате
vacancies = [vacancy1, vacancy2, vacancy3]
vacancies_sorted = sorted(vacancies)

print("\nВакансии отсортированы по зарплате:")
for v in vacancies_sorted:
    print(v)