from src.head_hunter_api import HeadHunterAPI


def filter_vacancies(vacancy_list, keywords) -> list:
    """Фильтрует вакансии по введенным словам."""

    # Приводим ключевые слова к нижнему регистру и разбиваем на список
    keywords = [keyword.lower() for keyword in keywords.split()]

    # Фильтруем вакансии
    filtered_vacancies = []
    for vacancy in vacancy_list:
        # Проверяем, содержится ли хотя бы одно ключевое слово в названии или описании вакансии
        if any(keyword in vacancy['title'].lower() or keyword in vacancy.get('description', '').lower() for keyword in
               keywords):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies

