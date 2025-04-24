from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.vacancy import Vacancy


class VacancyManager(ABC):
    """
    Абстрактный класс для управления вакансиями.
    """

    @abstractmethod
    def add_vacancy(self, new_vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs): # type: ignore
        """Получает вакансии из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: Vacancy) -> None:
        """Удаляет информацию о вакансии по указанному идентификатору."""
        pass
