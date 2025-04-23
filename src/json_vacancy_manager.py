import json

from src.head_hunter_api import settings_path
from src.vacancy import Vacancy
from src.vacancy_manager import VacancyManager


class JSONSaver(VacancyManager):
    """
    Класс для управления вакансиями с использованием JSON-файла.
    """

    def __init__(self, filename=settings_path):
        self.__filename = filename


    def get_vacancies(self, **kwargs):
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления вакансии в файл"""
        data = self.get_vacancies()
        # Проверяем, существует ли уже вакансия с таким же URL
        if any(item['url'] == vacancy._url for item in data):
            return  # Выходим из метода, если такая вакансия уже есть

        # Если вакансии с таким URL нет, добавляем новую
        data.append(vacancy)

        # Записываем обновленные данные обратно в файл
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def delete_vacancy(self, vacancy_id: Vacancy) -> None:
        """Удаляет информацию о вакансии."""
        data = self.get_vacancies()
        vacancy_url = vacancy_id.url  # Получаем URL из объекта Vacancy

        # Фильтруем вакансии, исключая ту, которую нужно удалить
        new_data = [item for item in data if item.get("url") != vacancy_url]

        # Если длина нового списка меньше, значит была удалена вакансия
        if len(new_data) < len(data):
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)

