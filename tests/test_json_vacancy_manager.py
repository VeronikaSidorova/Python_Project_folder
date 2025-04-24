import json
import os
import unittest
from unittest.mock import mock_open, patch

from src.json_vacancy_manager import JSONSaver


class TestJSONSaver(unittest.TestCase):
    def setUp(self): # type: ignore
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver(self.filename)

    def tearDown(self): # type: ignore
        # Удаляем файл после тестов
        if os.path.exists(self.filename):
            os.remove(self.filename)

    @patch("builtins.open", new_callable=mock_open)
    def test_get_vacancies_file_not_found(self, mock_file): # type: ignore
        mock_file.side_effect = FileNotFoundError
        vacancies = self.saver.get_vacancies()
        self.assertEqual(vacancies, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_get_vacancies_invalid_json(self, mock_file): # type: ignore
        mock_file.return_value.read.return_value = "invalid json"
        vacancies = self.saver.get_vacancies()
        self.assertEqual(vacancies, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_get_vacancies_valid_json(self, mock_file): # type: ignore
        mock_file.return_value.read.return_value = json.dumps(
            [
                {"title": "Программист", "url": "http://example.com/vacancy1"},
                {"title": "Дизайнер", "url": "http://example.com/vacancy2"},
            ]
        )

        vacancies = self.saver.get_vacancies()
        expected = [
            {"title": "Программист", "url": "http://example.com/vacancy1"},
            {"title": "Дизайнер", "url": "http://example.com/vacancy2"},
        ]

        self.assertEqual(vacancies, expected)
