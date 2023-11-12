import pandas as pd

# 1. Прочитайте файл
df = pd.read_csv("2017_jun_final.csv")

# 2. Прочитайте отриману таблицю
print(df.head())

# 3. Визначте розмір таблиці
print(df.shape)

# 4. Визначте типи всіх стовпців
print(df.dtypes)

# 5. Порахуйте, яка частка пропусків міститься в кожній колонці
print(df.isnull().sum() / len(df))


# 6. Видаліть усі стовпці з пропусками, крім стовпця "Мова програмування"
columns_to_drop = df.columns[df.isnull().sum() > 0].tolist()
columns_to_drop.remove("Язык.программирования")
print(columns_to_drop)
df.drop(columns=columns_to_drop, inplace=True)
print(df.head())

# 7. Перевірка частки пропусків після видалення
print(df.isnull().sum() / len(df))

# 8. Видаліть усі рядки з пропусками
df.dropna(inplace=True)

# 9. Новий розмір таблиці
print(df.shape)

# 10. Створіть нову таблицю python_data
python_data = df[df["Язык.программирования"] == "Python"]
# print(len(python_data))

# 11. Розмір таблиці python_data
print(python_data.shape)

# 12. Групування за стовпчиком "Посада"
grouped = python_data.groupby("Должность")

# 13. Агрегація даних за "Зарплата.в.місяць"
salary_stats = grouped["Зарплата.в.месяц"].agg(["min", "max"])
print(salary_stats)


# 14. Функція для обчислення середньої зарплати
def fill_avg_salary(row):
    return (row["min"] + row["max"]) / 2


# 15. Створення нового стовпчика "avg"
salary_stats["avg"] = salary_stats.apply(fill_avg_salary, axis=1)
print(salary_stats)

# 16. Описова статистика для нового стовпчика
print(salary_stats["avg"].describe())

# 17. Збереження отриманої таблиці в CSV файл
salary_stats.to_csv("salary_stats.csv")
