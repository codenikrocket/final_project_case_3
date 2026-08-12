



final_project_case_3/
├── exports/                # Папка для сохранённых сгенерированных файлов (CSV, JSON)
├── src/
│   ├── __init__.py
│   ├── generator.py        # Основная логика генерации данных (Faker + реалистичные связи)
│   ├── validators.py       # Валидация сгенерированных данных (код, сгенерированный ИИ)
│   ├── exporters.py         # Сохранение данных в CSV и JSON
│   ├── analytics.py        # Аналитика: распределение данных, построение графиков (matplotlib/seaborn)
│   ├── ml_quality.py       # ML-модель для оценки качества/реалистичности сгенерированных данных
│   └── ui.py               # Консольный интерфейс или базовый GUI/Streamlit
├── main.py                 # Точка входа в программу
├── requirements.txt        # Зависимости (faker, pandas, scikit-learn, matplotlib и др.)
├── .gitignore              # Исключения для Git
└── README.md               # Документация проекта