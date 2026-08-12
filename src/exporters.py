"""
Модуль для экспорта сгенерированных данных.
Поддерживает сохранение в форматы CSV и JSON.
"""

import json  # Импорт встроенного модуля для работы с форматом JSON
import csv   # Импорт встроенного модуля для работы с табличным форматом CSV
import os    # Импорт модуля для работы с операционной системой и путями файлов
from typing import List, Dict, Any  # Импорт типов для подсказок (type hinting)


class DataExporter:  # Объявление класса, отвечающего за экспорт данных
    """Класс для сохранения сгенерированных данных в файлы."""

    def __init__(self, export_dir: str = "exports"):  # Конструктор класса
        """
        Инициализация экспортера.
        :param export_dir: Название папки для сохранения файлов.
        """
        self.export_dir = export_dir  # Сохраняем имя целевой папки в атрибут объекта
        
        # Автоматическая проверка и создание папки экспорта
        if not os.path.exists(self.export_dir):  # Если такой папки на диске не существует
            os.makedirs(self.export_dir)  # Создаем эту папку

    def to_json(self, data: List[Dict[str, Any]], filename: str = "dataset.json") -> str:  # Метод экспорта в JSON
        """
        Сохраняет данные в формате JSON.
        """
        filepath = os.path.join(self.export_dir, filename)  # Безопасное склеивание пути к файлу (папка + имя)
        
        with open(filepath, "w", encoding="utf-8") as file:  # Открытие файла на запись с поддержкой кириллицы
            # Запись данных с отступами (indent=4) и отключением экранирования не-ASCII символов
            json.dump(data, file, ensure_ascii=False, indent=4)  
            
        return filepath  # Возвращаем итоговый путь к файлу (пригодится для вывода в консоль)

    def to_csv(self, data: List[Dict[str, Any]], filename: str = "dataset.csv") -> str:  # Метод экспорта в CSV
        """
        Сохраняет данные в формате CSV.
        """
        if not data:  # Проверка на случай, если передан пустой список данных
            return ""  # Прерываем работу, чтобы не создавать пустой файл с ошибкой

        filepath = os.path.join(self.export_dir, filename)  # Формирование пути к CSV-файлу
        headers = list(data[0].keys())  # Получение списка заголовков (берем ключи из первого словаря данных)
        
        # Открытие файла на запись (newline="" предотвращает появление лишних пустых строк в Windows)
        with open(filepath, "w", encoding="utf-8-sig", newline="") as file:  
            writer = csv.DictWriter(file, fieldnames=headers)  # Создание объекта для записи словарей в CSV по заголовкам
            writer.writeheader()  # Физическая запись первой строки с названиями колонок
            writer.writerows(data)  # Запись всех остальных строк с самими данными
            
        return filepath  # Возвращаем путь к файлу


# Блок для быстрого тестирования работы модуля
if __name__ == "__main__":  # Если файл запущен напрямую
    # Создаем фиктивные данные для проверки
    sample_data = [
        {"full_name": "Иванов Иван", "email": "ivan@example.com", "age": 30},
        {"full_name": "Петрова Анна", "email": "anna@example.com", "age": 25}
    ]
    
    exporter = DataExporter()  # Инициализация нашего класса
    json_path = exporter.to_json(sample_data, "test_data.json")  # Тестовый экспорт в JSON
    csv_path = exporter.to_csv(sample_data, "test_data.csv")  # Тестовый экспорт в CSV
    
    print(f"Файлы успешно сохранены:\n{json_path}\n{csv_path}")  # Вывод путей к созданным файлам