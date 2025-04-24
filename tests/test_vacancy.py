import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_valid_vacancy_creation(self): # type: ignore
        """Тест успешного создания объекта Vacancy."""
        vacancy = Vacancy("Программист", "http://example.com/vacancy", "от 100000", "Компания A")
        self.assertEqual(vacancy._title, "Программист")
        self.assertEqual(vacancy._url, "http://example.com/vacancy")
        self.assertEqual(vacancy._salary_str, "от 100000")
        self.assertEqual(vacancy._salary, 100000.0)
        self.assertEqual(vacancy._company, "Компания A")

    def test_invalid_title(self): # type: ignore
        """Тест создания объекта Vacancy с некорректным названием."""
        with self.assertRaises(ValueError) as context:
            Vacancy("", "http://example.com/vacancy", "от 100000", "Компания A")
        self.assertEqual(str(context.exception), "Название вакансии должно быть непустой строкой.")

    # def test_invalid_salary(self):
    #     """Тест создания объекта Vacancy с некорректной зарплатой."""
    #     with self.assertRaises(ValueError) as context:
    #         Vacancy("Программист", "http://example.com/vacancy", "-50000", "Компания A")
    #     self.assertEqual(str(context.exception), "Зарплата должна быть неотрицательным числом. Получено: -50000.0")

    def test_parse_salary(self): # type: ignore
        """Тест метода parse_salary."""
        self.assertEqual(Vacancy.parse_salary("от 100000"), 100000.0)
        self.assertEqual(Vacancy.parse_salary("до 150000"), 150000.0)
        self.assertEqual(Vacancy.parse_salary("100000-150000"), 100000.0)
        self.assertEqual(Vacancy.parse_salary("не указана"), 0.0)

    def test_cast_to_object_list(self): # type: ignore
        """Тест метода cast_to_object_list."""
        vacancies_data = [
            {
                "name": "Программист",
                "alternate_url": "http://example.com/vacancy",
                "salary": {"from": 100000, "currency": "RUB"},
                "employer": {"name": "Компания A"},
            },
            {
                "name": "Тестировщик",
                "alternate_url": "http://example.com/vacancy2",
                "salary": {"to": 80000, "currency": "RUB"},
                "employer": {"name": "Компания B"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        self.assertEqual(len(vacancies), 2)

        # Проверяем первый объект
        self.assertEqual(vacancies[0]._title, "Программист")
        self.assertEqual(vacancies[0]._salary_str, "от 100000 RUB")

        # Проверяем второй объект
        self.assertEqual(vacancies[1]._title, "Тестировщик")
        self.assertEqual(vacancies[1]._salary_str, "до 80000 RUB")

    def test_to_dict(self): # type: ignore
        """Тест метода to_dict."""
        vacancy = Vacancy("Программист", "http://example.com/vacancy", "от 100000", "Компания A")

        expected_dict = {
            "_title": "Программист",
            "_url": "http://example.com/vacancy",
            "_salary_str": "от 100000",
            "_salary": 100000.0,
            "_company": "Компания A",
        }

        self.assertEqual(vacancy.to_dict(), expected_dict)
