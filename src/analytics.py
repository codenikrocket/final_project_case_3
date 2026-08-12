"""
Модуль аналитики сгенерированных данных.
Строит графики распределения и сохраняет их в виде изображений.
"""

import os  # Импорт модуля для работы с путями и файловой системой
import pandas as pd  # Импорт pandas для удобной работы с табличными данными (алиас pd)
import matplotlib.pyplot as plt  # Импорт модуля matplotlib для построения графиков
import seaborn as sns  # Импорт seaborn для создания красивых статистических графиков
from typing import List, Dict, Any  # Импорт типов для аннотаций


class DataAnalyzer:  # Объявление класса-анализатора
    """Класс для анализа и визуализации сгенерированных данных."""

    def __init__(self, export_dir: str = "exports"):  # Конструктор класса
        """Инициализация анализатора."""
        self.export_dir = export_dir  # Сохранение пути к папке сохранения графиков
        
        if not os.path.exists(self.export_dir):  # Проверка существования целевой папки
            os.makedirs(self.export_dir)  # Создание папки, если её нет

        # Настройка глобального стиля графиков seaborn для эстетики
        sns.set_theme(style="whitegrid")  # Включение белого фона со светлой сеткой

    def _get_dataframe(self, data: List[Dict[str, Any]]) -> pd.DataFrame:  # Вспомогательный метод
        """Конвертирует список словарей в DataFrame для удобного анализа."""
        return pd.DataFrame(data)  # Преобразование массива JSON-подобных объектов в таблицу pandas

    def plot_age_distribution(self, data: List[Dict[str, Any]], filename: str = "age_distribution.png"):  # Метод для графика возраста
        """Строит гистограмму распределения возраста и сохраняет в файл."""
        df = self._get_dataframe(data)  # Получение табличного представления данных
        
        if df.empty or "age" not in df.columns:  # Защита от пустых данных или отсутствия нужной колонки
            return  # Прерывание функции, если данных нет

        plt.figure(figsize=(10, 6))  # Создание холста для графика размером 10x6 дюймов
        # Построение гистограммы распределения колонки 'age' с линией тренда (kde=True)
        sns.histplot(data=df, x="age", bins=15, kde=True, color="skyblue")  
        
        plt.title("Распределение возраста пользователей")  # Установка заголовка графика
        plt.xlabel("Возраст (лет)")  # Подпись горизонтальной оси
        plt.ylabel("Количество")  # Подпись вертикальной оси
        
        filepath = os.path.join(self.export_dir, filename)  # Формирование пути для сохранения картинки
        plt.savefig(filepath, bbox_inches="tight")  # Сохранение графика в файл (tight обрезает лишние белые поля)
        plt.close()  # Закрытие графика в памяти, чтобы не расходовать ресурсы

    def plot_gender_distribution(self, data: List[Dict[str, Any]], filename: str = "gender_distribution.png"):  # Метод для графика полов
        """Строит круговую диаграмму распределения полов и сохраняет в файл."""
        df = self._get_dataframe(data)  # Получение табличного представления данных
        
        if df.empty or "gender" not in df.columns:  # Проверка наличия данных и колонки пола
            return  # Выход, если строить не из чего

        gender_counts = df["gender"].value_counts()  # Подсчет количества уникальных значений (сколько мужчин/женщин)
        
        plt.figure(figsize=(8, 8))  # Создание квадратного холста 8x8 дюймов для круговой диаграммы
        # Построение диаграммы с выводом процентов (autopct) и кастомными цветами
        # Стало (с явным преобразованием в список):
        plt.pie(gender_counts, labels=gender_counts.index.tolist(), autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"])
        
        plt.title("Соотношение полов")  # Заголовок диаграммы
        
        filepath = os.path.join(self.export_dir, filename)  # Формирование пути сохранения
        plt.savefig(filepath, bbox_inches="tight")  # Сохранение диаграммы в PNG
        plt.close()  # Очистка памяти


# Блок для быстрого тестирования работы модуля
if __name__ == "__main__":  # Проверка прямого запуска файла
    # Тестовые данные-заглушки (только необходимые колонки для графиков)
    sample_data = [
        {"age": 25, "gender": "Мужской"},
        {"age": 30, "gender": "Женский"},
        {"age": 22, "gender": "Мужской"},
        {"age": 35, "gender": "Женский"},
        {"age": 40, "gender": "Мужской"},
        {"age": 45, "gender": "Мужской"},
        {"age": 28, "gender": "Женский"},
    ]
    
    analyzer = DataAnalyzer()  # Инициализация класса аналитики
    analyzer.plot_age_distribution(sample_data)  # Вызов генерации графика возраста
    analyzer.plot_gender_distribution(sample_data)  # Вызов генерации графика полов
    
    print("Тестовые графики успешно сохранены в папку exports/")  # Вывод подтверждения в терминал