"""
Модуль валидации сгенерированных данных.
Содержит функции для проверки форматов email и дат.
"""

import re  # Импорт модуля регулярных выражений
from datetime import datetime  # Импорт класса для работы с датами

def is_valid_email(email: str) -> bool:  # Объявление функции проверки email
    """Проверяет email с помощью регулярного выражения."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Шаблон корректного адреса
    return bool(re.match(pattern, email))  # Возврат True при совпадении

def is_valid_date(date_str: str) -> bool:  # Объявление функции проверки даты
    """Проверяет, соответствует ли дата формату ДД.ММ.ГГГГ."""
    try:  # Начало блока перехвата ошибок
        datetime.strptime(date_str, "%d.%m.%Y")  # Парсинг строки в нашем формате
        return True  # Возврат True, если ошибка не возникла
    except ValueError:  # Перехват ошибки неверного формата
        return False  # Возврат False при ошибке

def validate_dataset(data: list) -> dict:  # Объявление функции проверки списка
    """Проверяет весь список сгенерированных данных и возвращает статистику."""
    errors = 0  # Инициализация счетчика ошибок
    
    for person in data:  # Цикл по всем записям в датасете
        if not is_valid_email(person.get("email", "")):  # Проверка email записи
            errors += 1  # Увеличение счетчика при ошибке
            
        if not is_valid_date(person.get("birth_date", "")):  # Проверка даты рождения
            errors += 1  # Увеличение счетчика при ошибке
            
    return {  # Возврат итогового словаря
        "total_records": len(data),  # Общее число проверенных записей
        "errors_found": errors,  # Количество найденных ошибок
        "is_valid": errors == 0  # Флаг успешной проверки (ошибок нет)
    }

# Быстрый тест модуля
if __name__ == "__main__":  # Проверка запуска файла напрямую
    test_email = "ivan.petrov@gmail.com"  # Корректный email
    test_date = "15.08.2026"  # Корректная дата
    print(f"Email valid: {is_valid_email(test_email)}")  # Вывод результата проверки email
    print(f"Date valid: {is_valid_date(test_date)}")  # Вывод результата проверки даты