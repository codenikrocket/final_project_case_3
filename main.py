"""
Главный файл запуска приложения.
Оркестрирует работу всех модулей: от запроса данных у пользователя до экспорта и аналитики.
"""

# Импорт всех наших написанных модулей из пакета src
from src.ui import get_user_input  # Импорт функции интерфейса
from src.generator import DataGenerator  # Импорт класса генератора
from src.validators import validate_dataset  # Импорт функции валидации
from src.exporters import DataExporter  # Импорт класса экспорта
from src.analytics import DataAnalyzer  # Импорт класса аналитики
from src.ml_quality import DataQualityChecker  # Импорт класса проверки качества

def main():  # Главная функция программы
    # 1. Запрос настроек у пользователя
    settings = get_user_input()  
    count = settings["count"]
    export_format = settings["format"]

    print(f"\n[1/5] Запуск генерации {count} записей...")
    # 2. Инициализация генератора и создание данных
    generator = DataGenerator()  
    data = generator.generate_dataset(count)

    print("[2/5] Валидация сгенерированных данных...")
    # 3. Базовая проверка форматов (email, даты)
    validation_results = validate_dataset(data)

    print("[3/5] ML-оценка реалистичности (поиск аномалий)...")
    # 4. Проверка качества через алгоритм машинного обучения
    ml_checker = DataQualityChecker()
    ml_results = ml_checker.evaluate_quality(data)

    print("[4/5] Построение аналитических графиков...")
    # 5. Генерация и сохранение графиков в папку exports/
    analyzer = DataAnalyzer()
    analyzer.plot_age_distribution(data)
    analyzer.plot_gender_distribution(data)

    print(f"[5/5] Экспорт данных в формат(ы): {export_format}...")
    # 6. Сохранение данных в выбранных форматах
    exporter = DataExporter()
    if export_format in ["csv", "all"]:
        exporter.to_csv(data)
    if export_format in ["json", "all"]:
        exporter.to_json(data)

    # 7. Финальный вывод красивого отчета о проделанной работе
    print("\n" + "=" * 50)
    print("ИТОГОВЫЙ ОТЧЁТ О РАБОТЕ")
    print("=" * 50)
    print(f"Сгенерировано записей: {count}")
    print(f"Ошибок валидации (форматы): {validation_results['errors_found']}")
    print(f"Найдено ML-аномалий: {ml_results['anomalies_found']}")
    print(f"Показатель реалистичности (ML Score): {ml_results['quality_score']}%")
    print("Графики распределения сохранены в папку 'exports/'")
    print("=" * 50 + "\n")

if __name__ == "__main__":  # Точка входа в программу
    main()  # Запуск главной функции