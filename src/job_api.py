from abc import ABC, abstractmethod


class JobAPI(ABC):

    @abstractmethod
    def _connect(self): # type: ignore
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """Метод для получения вакансий по ключевому слову."""
        pass
