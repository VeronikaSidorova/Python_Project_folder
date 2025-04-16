import json
from typing import List, Dict, Any

from src.vacancy_manager import VacancyManager


class JSONVacancyManager(VacancyManager):
    """
    Класс для управления вакансиями с использованием JSON-файла.
    """

    def __init__(self, filename: str):
        self.filename = filename

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию в JSON-файл."""
        vacancies = self._load_vacancies()
        vacancies.append(vacancy)
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получает вакансии из файла по указанным критериям."""
        vacancies = self._load_vacancies()

        # Фильтрация вакансий по критериям
        filtered_vacancies = [
            vacancy for vacancy in vacancies
            if all(vacancy.get(key) == value for key, value in criteria.items())
        ]

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансии по указанному идентификатору."""
        vacancies = self._load_vacancies()

        # Удаляем вакансию с указанным идентификатором
        vacancies = [vacancy for vacancy in vacancies if vacancy.get('id') != vacancy_id]

        self._save_vacancies(vacancies)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загружает вакансии из JSON-файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохраняет вакансии в JSON-файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)