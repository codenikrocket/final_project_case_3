"""
Модуль оценки качества сгенерированных данных с помощью машинного обучения.
Использует IsolationForest для поиска аномалий (выбросов).
"""

import pandas as pd  # Импорт библиотеки pandas для удобной работы с таблицами
from sklearn.ensemble import IsolationForest  # Импорт алгоритма поиска аномалий "Изолирующий лес"
from typing import List, Dict, Any  # Импорт типов для аннотаций функций


class DataQualityChecker:  # Объявление класса проверки качества данных
    """Класс для ML-оценки реалистичности сгенерированного датасета."""

    def __init__(self, contamination: float = 0.05):  # Конструктор с параметром доли ожидаемых аномалий (по умолчанию 5%)
        """
        Инициализация ML-модели.
        :param contamination: Ожидаемая доля аномалий в датасете.
        """
        # Создание экземпляра модели с фиксацией random_state для одинаковых результатов при перезапусках
        self.model = IsolationForest(contamination=contamination, random_state=42)  

    def evaluate_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:  # Основной метод оценки качества
        """
        Анализирует данные и возвращает статистику по аномалиям.
        """
        if not data:  # Проверка на пустой список входных данных
            return {"error": "Нет данных для анализа"}  # Возврат ошибки, если данных нет

        df = pd.DataFrame(data)  # Преобразование списка словарей в таблицу (DataFrame) pandas
        
        # Подготовка числовых признаков (фичей) для ML-модели
        if "age" not in df.columns or "email" not in df.columns:  # Проверка наличия нужных колонок
            return {"error": "Отсутствуют необходимые колонки (age, email)"}  # Выход, если колонок нет

        # ML-модели нужны числа, поэтому создаем новый признак - длину email
        df["email_length"] = df["email"].apply(len)  # Вычисление и запись длины каждого email-адреса

        # Отбираем только числовые колонки для обучения (возраст и длина почты)
        features = df[["age", "email_length"]]  # Создание отдельной таблицы с признаками

        # Обучение модели и предсказание (1 - норма, -1 - аномалия)
        df["anomaly_score"] = self.model.fit_predict(features)  # Применение алгоритма и запись результатов в новую колонку
        
        # Подсчет результатов
        anomalies = df[df["anomaly_score"] == -1]  # Фильтрация строк, которые модель признала аномалиями
        normal_count = len(df) - len(anomalies)  # Вычисление количества нормальных записей

        return {  # Возврат словаря с результатами ML-анализа
            "total_records": len(df),  # Общее количество проанализированных записей
            "normal_records": normal_count,  # Количество реалистичных записей
            "anomalies_found": len(anomalies),  # Количество найденных алгоритмом аномалий
            "quality_score": round((normal_count / len(df)) * 100, 2)  # Расчет процента "качества" датасета (округление до 2 знаков)
        }


# Блок для быстрого тестирования работы модуля
if __name__ == "__main__":  # Проверка запуска файла напрямую (не через import)
    # Тестовые данные (последняя запись - явная аномалия: невероятный возраст и длиннющий email)
    sample_data = [
        {"age": 25, "email": "ivan.petrov@gmail.com"},
        {"age": 30, "email": "anna.s@yandex.ru"},
        {"age": 22, "email": "max@mail.ru"},
        {"age": 35, "email": "elena.k@example.com"},
        {"age": 40, "email": "dmitry.v@outlook.com"},
        {"age": 45, "email": "sergey.m@rambler.ru"},
        {"age": 120, "email": "a" * 50 + "@strange.com"}  # Искусственная аномалия для проверки ML
    ]
    
    checker = DataQualityChecker(contamination=0.14)  # Инициализация с ожиданием ~14% аномалий (1 из 7 записей)
    result = checker.evaluate_quality(sample_data)  # Запуск анализа тестовых данных
    
    import pprint  # Импорт модуля для красивого вывода словарей
    print("\nРезультаты ML-оценки:")  # Вывод заголовка
    pprint.pprint(result)  # Печать итоговой статистики в консоль