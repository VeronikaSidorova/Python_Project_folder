import unittest
from unittest.mock import MagicMock
from src.vacancy import Vacancy
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies  # Замените your_module на имя вашего модуля

class TestVacancyFunctions(unittest.TestCase):

    def setUp(self):
        # Создаем несколько фиктивных вакансий для тестирования
        self.vacancy1 = Vacancy("Программист", "http://example.com/vacancy1", "100000", "Компания A")
        self.vacancy2 = Vacancy("Аналитик", "http://example.com/vacancy2", "80000", "Компания B")
        self.vacancy3 = Vacancy("Менеджер проектов", "http://example.com/vacancy3", "None", "Компания C")
        self.vacancies = [self.vacancy1, self.vacancy2, self.vacancy3]

    def test_filter_vacancies(self):
        filter_words = ["программист"]
        filtered = filter_vacancies(self.vacancies, filter_words)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]._title, "Программист")

    def test_get_vacancies_by_salary(self):
        salary_range = "70000-90000"
        ranged = get_vacancies_by_salary(self.vacancies, salary_range)
        self.assertEqual(len(ranged), 1)
        self.assertEqual(ranged[0]._title, "Аналитик")

    def test_sort_vacancies(self):
        sorted_vacs = sort_vacancies(self.vacancies)
        self.assertEqual(sorted_vacs[0]._title, "Программист")
        self.assertEqual(sorted_vacs[1]._title, "Аналитик")
        self.assertEqual(sorted_vacs[2]._title, "Менеджер проектов")

    def test_get_top_vacancies(self):
        top_n = 2
        top_vacs = get_top_vacancies(self.vacancies, top_n)
        self.assertEqual(len(top_vacs), 2)
        self.assertEqual(top_vacs[0]._title, "Программист")
        self.assertEqual(top_vacs[1]._title, "Аналитик")

    def test_print_vacancies(self):
        # Для тестирования вывода на экран можно использовать unittest.mock.patch
        with unittest.mock.patch('builtins.print') as mock_print:
            print_vacancies(self.vacancies)
            mock_print.assert_any_call("Название: Программист, Компания: Компания A, Зарплата: 100000.0")
            mock_print.assert_any_call("Название: Аналитик, Компания: Компания B, Зарплата: 80000.0")
            mock_print.assert_any_call("Название: Менеджер проектов, Компания: Компания C, Зарплата: Не указана")