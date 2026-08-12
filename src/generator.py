"""
Модуль генерации тестовых данных с помощью библиотеки Faker.
Обеспечивает реалистичные взаимосвязи между полями (например, name -> email).
"""

import random  # Импорт модуля для генерации случайных чисел и элементов
from datetime import datetime, date  # Импорт классов для работы с датой и временем
from typing import List, Dict, Any  # Импорт типов для аннотации функций
from faker import Faker  # Импорт библиотеки Faker для создания фейковых данных


class DataGenerator:  # Объявление класса-генератора данных
    """Класс для генерации реалистичных персональных тестовых данных."""

    def __init__(self, locale: str = "ru_RU"):  # Конструктор класса с локалью по умолчанию
        """
        Инициализация генератора.
        :param locale: Локаль Faker (по умолчанию 'ru_RU').
        """
        self.fake = Faker(locale)  # Создание экземпляра Faker с выбранным языком
        # Набор популярных почтовых доменов для реалистичности
        self.email_domains = [  # Перечень доменов для формирования email
            "gmail.com",
            "yandex.ru",
            "mail.ru",
            "rambler.ru",
            "outlook.com",
            "example.com",
        ]

    def _transliterate(self, text: str) -> str:  # Вспомогательный метод транслитерации
        """Простая транслитерация кириллицы в латиницу для создания email."""
        translit_dict = {  # Словарь соответствия кириллических букв латинским
            "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
            "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
            "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
            "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
            "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya"
        }
        result = []  # Список для сборки символов латиницы
        for char in text.lower():  # Цикл по каждому символу входного текста в нижнем регистре
            result.append(translit_dict.get(char, char))  # Замена буквы по словарю или сохранение оригинала
        return "".join(result)  # Объединение символов списка в единую строку

    def _generate_realistic_email(self, first_name: str, last_name: str) -> str:  # Метод сборки логичного email
        """
        Генерирует email на основе имени и фамилии.
        Пример: ivan.petrov@gmail.com
        """
        clean_first = self._transliterate(first_name).replace(" ", "")  # Очистка и транслитерация имени
        clean_last = self._transliterate(last_name).replace(" ", "")  # Очистка и транслитерация фамилии
        
        domain = random.choice(self.email_domains)  # Случайный выбор почтового домена из списка
        
        # Различные шаблоны email
        patterns = [  # Список шаблонов структуры почтового адреса
            f"{clean_first}.{clean_last}@{domain}",
            f"{clean_first[0]}{clean_last}@{domain}",
            f"{clean_last}.{clean_first}@{domain}",
            f"{clean_first}_{clean_last}{random.randint(10, 99)}@{domain}"
        ]
        return random.choice(patterns)  # Случайный выбор одного из вариантов email

    def generate_person(self) -> Dict[str, Any]:  # Метод генерации профиля одного человека
        """
        Генерирует одну запись персональных данных.
        :return: Словарь с данными.
        """
        gender = random.choice(["male", "female"])  # Случайный выбор пола
        
        if gender == "male":  # Проверка, если выбран мужской пол
            first_name = self.fake.first_name_male()  # Генерация мужского имени
            last_name = self.fake.last_name_male()  # Генерация мужской фамилии
        else:  # Если пол женский
            first_name = self.fake.first_name_female()  # Генерация женского имени
            last_name = self.fake.last_name_female()  # Генерация женской фамилии

        email = self._generate_realistic_email(first_name, last_name)  # Создание почты на базе имени и фамилии
        birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=70)  # Генерация даты рождения (18-70 лет)
        
        # Расчет возраста на текущий момент
        today = date.today()  # Получение сегодняшней даты
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))  # Вычисление возраста

        return {  # Возврат словаря с полным набором сгенерированных полей
            "full_name": f"{last_name} {first_name}",  # Объединение фамилии и имени
            "first_name": first_name,  # Имя
            "last_name": last_name,  # Фамилия
            "gender": "Мужской" if gender == "male" else "Женский",  # Преобразование пола в понятный вид
            "email": email,  # Персональный email
            "phone": self.fake.phone_number(),  # Генерация номера телефона
            "address": self.fake.address().replace("\n", ", "),  # Генерация адреса в одну строку
            
            # ИЗМЕНЁННЫЕ СТРОКИ:
            "birth_date": birth_date.strftime("%d.%m.%Y"),  # Форматирование даты рождения в ДД.ММ.ГГГГ
            "age": age,  # Вычисленный возраст
            "job": self.fake.job(),  # Генерация профессии
            "company": self.fake.company(),  # Генерация названия компании
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Текущая дата и время создания записи (ДД.ММ.ГГГГ ЧЧ:ММ:СС)
        }

    def generate_dataset(self, count: int) -> List[Dict[str, Any]]:  # Метод генерации множества записей
        """
        Генерирует список записей.
        :param count: Количество записей.
        :return: Список словарей.
        """
        return [self.generate_person() for _ in range(count)]  # Генерация списка из count объектов через List Comprehension


# Быстрый тест модуля при прямом запуске
if __name__ == "__main__":  # Проверка прямого запуска файла (не при импорте)
    generator = DataGenerator(locale="ru_RU")  # Создание объекта генератора
    sample_data = generator.generate_dataset(3)  # Генерация 3 тестовых записей
    import pprint  # Импорт модуля красивого вывода
    pprint.pprint(sample_data)  # Вывод сгенерированных данных в консоль