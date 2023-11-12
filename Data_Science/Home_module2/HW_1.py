import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


url = "https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8"
tables = pd.read_html(
    url,
    match=re.compile(
        r"^Коефіцієнт народжуваності в регіонах України \(1950\—2019\)*$", re.I
    ),
)

# Припускаючи, що потрібна таблиця - перша на сторінці
df = tables[0]

# Вивести перші рядки таблиці
print(df.head())
print(df.columns)
# Визначте кількість рядків та стовпців
print(df.shape)

# Замініть у таблиці значення "—" на NaN
df.replace("—", np.nan, inplace=True)
print(df.isnull().sum())
# print((df == "—").sum())

# Визначте типи всіх стовпців
print(df.dtypes)

# Конвертація типів нечислових колонок у числові
for col in df.columns:
    if col != "Регіон":
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="coerce")

# Частка пропусків у кожній колонці
print(df.isnull().sum() / df.shape[0])

# Видалення даних по всій країні (останній рядок)
df.drop(df.tail(1).index, inplace=True)

# Заміна відсутніх даних середніми значеннями
df.fillna(df.mean(numeric_only=True), inplace=True)
print(df)

# Регіони з вищим рівнем народжуваності за середній у 2019 році
mean_birthrate_2019 = df["2019"].mean()
print(mean_birthrate_2019)
print(df["2019"].dtypes)
regions_higher_birthrate = df[df["2019"] > mean_birthrate_2019]["Регіон"].tolist()
print(regions_higher_birthrate)

# Регіон з найвищою народжуваністю у 2014 році
highest_birthrate_2014_region = df[df["2014"] == df["2014"].max()]["Регіон"].iloc[0]
print(highest_birthrate_2014_region)

# Стовпчикова діаграма народжуваності по регіонах у 2019 році
df.set_index("Регіон")["2019"].plot(kind="bar")
plt.ylabel("Народжуваність")
plt.title("Народжуваність по регіонах України у 2019 році")
plt.show()
