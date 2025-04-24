import unittest
from unittest.mock import MagicMock, patch

import requests

from src.head_hunter_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch("requests.Session.get")
    def test_connect_success(self, mock_get): # type: ignore
        """Тест успешного подключения к API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api._connect()

        self.assertTrue(result)
        mock_get.assert_called_once_with(HeadHunterAPI.BASE_URL)

    @patch("requests.Session.get")
    def test_connect_failure(self, mock_get): # type: ignore
        """Тест неудачного подключения к API"""
        mock_get.side_effect = requests.RequestException("Ошибка подключения")

        api = HeadHunterAPI()
        result = api._connect()

        self.assertFalse(result)

    @patch("requests.Session.get")
    def test_get_vacancies_success(self, mock_get): # type: ignore
        """Тест успешного получения вакансий"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "Вакансия 1"}, {"id": "2", "name": "Вакансия 2"}]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Тест")

        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Вакансия 1")
        self.assertEqual(vacancies[1]["name"], "Вакансия 2")
        mock_get.assert_called_once_with(api.BASE_URL, params={"text": "Тест", "per_page": 20})

    @patch("requests.Session.get")
    def test_get_vacancies_failure(self, mock_get): # type: ignore
        """Тест неудачного получения вакансий"""
        mock_get.side_effect = requests.RequestException("Ошибка при получении вакансий")

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Тест")

        self.assertEqual(len(vacancies), 0)
