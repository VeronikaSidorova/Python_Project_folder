import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VacancyManager(ABC):
    """
    Абстрактный класс для управления вакансиями.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получает вакансии из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаляет информацию о вакансии по указанному идентификатору."""
        pass
