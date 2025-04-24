from src.head_hunter_api import HeadHunterAPI
from src.vacancy import Vacancy


def filter_vacancies(vacancies, filter_words):
    """Фильтрует вакансии по ключевым словам."""
    filtered = []
    for vacancy in vacancies:
        if any(word.lower() in vacancy._title.lower() for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies, salary_range):
    """Фильтрует вакансии по диапазону зарплат."""
    min_salary, max_salary = map(int, salary_range.split('-'))
    ranged = []

    for vacancy in vacancies:
        if vacancy._salary is not None and min_salary <= vacancy._salary <= max_salary:
            ranged.append(vacancy)
    return ranged

def sort_vacancies(vacancies):
    """Сортирует вакансии по зарплате (по убыванию)."""
    if vacancies is None or not vacancies:
        return []  # Возвращаем пустой список, если vacancies None или пустой

    return sorted(vacancies, key=lambda x: x._salary if x._salary is not None else 0, reverse=True)

def get_top_vacancies(vacancies, top_n):
    """Возвращает топ N вакансий."""
    return vacancies[:top_n]

def print_vacancies(vacancies):
    """Выводит вакансии на экран."""
    if not vacancies:
        print("Нет доступных вакансий.")
        return
    for vacancy in vacancies:
        print(f"Название: {vacancy._title}, Компания: {vacancy._company}, Зарплата: {vacancy._salary if vacancy._salary else 'Не указана'}")

