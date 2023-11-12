import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Прочитайте файл
df = pd.read_csv("bestsellers with categories.csv")

print(df.columns, "\n")

print(df.head(), "\n")

# Визначте розмір таблиці
print(df.shape, "\n")

# датасет містить інформацію про 550 книг.

df.columns = ["name", "author", "user_rating", "reviews", "price", "year", "genre"]
print(df.columns, "\n")

print(df.isna().sum(), "\n")

# Чи є в якихось змінних пропуски? -- Ні

# унікальні жанри -- ['Non Fiction' 'Fiction']
unique_genres = df["genre"].unique()
print(unique_genres, "\n")

# Побудова гістограми для стовпця "ціна"
sns.set()
df["price"].plot(kind="hist", color="skyblue", edgecolor="black", rwidth=0.92)

# Назви для осі
plt.xlabel("price")
plt.ylabel("Кількість")
plt.title("Розподіл цін")
plt.grid(True)
plt.show()

# Максимальна ціна
max_price = df["price"].max()
print(f"Максимальна ціна: {max_price}", "\n")

# Мінімальна ціна
min_price = df["price"].min()
print(f"Мінімальна ціна: {min_price}", "\n")

# Середня ціна
mean_price = df["price"].mean()
print(f"Середня ціна: {mean_price}", "\n")

# Медіанна ціна
median_price = df["price"].median()
print(f"Медіанна ціна: {median_price}", "\n")

# Який рейтинг у датасеті найвищий?
max_user_rating = df["user_rating"].max()
print(f"Найвищій рейтінг: {max_user_rating}", "\n")

# Підраховуємо, скільки книг мають цей максимальний рейтинг
num_books_max_rating = df[df["user_rating"] == max_user_rating].shape[0]
print(f"Кількість книг з максимальним рейтингом: {num_books_max_rating}", "\n")


# Яка книга має найбільше відгуків?
max_reviews = df["reviews"].max()
book_with_max_reviews = df[df["reviews"] == max_reviews]["name"]
print("Книга(и) з найбільшою кількістю відгуків:", "\n")
print(book_with_max_reviews, "\n")

# Топ-50 у 2015 році, яка книга найдорожча
top_50 = df[df["year"] == 2015]
top_50_books_2015 = top_50.sort_values(by="user_rating", ascending=False).head(50)
most_expensive_book = top_50_books_2015[
    top_50_books_2015["price"] == top_50_books_2015["price"].max()
]
print("Найдорожча книга у топ-50 у 2015 році:", "\n")
print(most_expensive_book[["name", "price"]], "\n")


# Скільки книг жанру Fiction потрапили до Топ-50 у 2010 році?
fiction_books_2010 = df[(df["year"] == 2010) & (df["genre"] == "Fiction")].head(50)
num_fiction_books = fiction_books_2010.shape[0]
print(num_fiction_books, "\n")


# Скільки книг з рейтингом 4.9 потрапило до рейтингу у 2010 та 2011 роках?
books_rating_4_9 = df[
    (df["user_rating"] == 4.9) & ((df["year"] == 2010) | (df["year"] == 2011))
]
num_books = books_rating_4_9.shape[0]
print(
    f"Книг з рейтингом 4.9 потрапило до рейтингу у 2010 та 2011 роках : {num_books}",
    "\n",
)

# №2
books_rating_4_9 = df[(df["user_rating"] == 4.9) & (df["year"].isin([2010, 2011]))]
num_books = books_rating_4_9.shape[0]
print(
    f"Книг з рейтингом 4.9 потрапило до рейтингу у 2010 та 2011 роках : {num_books}",
    "\n",
)


# відсортуємо за зростанням ціни всі книги, які потрапили до рейтингу в 2015 році і коштують дешевше за 8 доларів.
books_2015_under_8 = df[(df["year"] == 2015) & (df["price"] < 8)].sort_values(
    by="price", ascending=True
)
print(f"Top-50 книг що коштують дешевше 8 долларів: {books_2015_under_8}", "\n")

# Вибір останньої книги в відсортованому списку
print(books_2015_under_8.iloc[-1], "\n")


"""Друга частина"""


# Групування даних за жанром і обчислення мінімальних та максимальних цін
price_stats = df.groupby("genre")["price"].agg(["min", "max"])

for genre in unique_genres:
    print(f"Максимальна ціна для жанру {genre}: {price_stats.loc[genre, 'max']}")
    print(f"Мінімальна ціна для жанру {genre}: {price_stats.loc[genre, 'min']}", "\n")


# новий датафрейм, який вміщатиме кількість книг для кожного з авторів.
author_books_count = df.groupby("author")["name"].count().reset_index(name="book_count")

print(f"Розмірність таблиці: {author_books_count.shape}")
print(author_books_count.dtypes)

most_books_author = author_books_count["book_count"].idxmax()
author_name = author_books_count.loc[most_books_author, "author"]
print(f"Автор з найбільшою кількістю книг: {author_name}")

num_books = author_books_count.loc[most_books_author, "book_count"]
print(f"Кількість книг цього автора: {num_books}")


author_avg_rating = (
    df.groupby("author")["user_rating"].mean().reset_index(name="avg_rating")
)

min_rating_author = author_avg_rating["avg_rating"].idxmin()
author_name = author_avg_rating.loc[min_rating_author, "author"]
min_avg_rating = author_avg_rating.loc[min_rating_author, "avg_rating"]

print(f"Автор з мінімальним середнім рейтингом: {author_name}")
print(f"Середній рейтинг цього автора: {min_avg_rating}")


# Об'єднання DataFrame
combined_df = pd.concat(
    [author_books_count.set_index("author"), author_avg_rating.set_index("author")],
    axis=1,
)

# Відсортування об'єднаного DataFrame
sorted_df = combined_df.sort_values(
    by=["book_count", "avg_rating"], ascending=[True, True]
)
first_author = sorted_df.index[0]

print(f"Перший автор у списку: {first_author}")


# print(np.sort(df["year"].unique()))


"""Графіки"""

# 1
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="user_rating", y="reviews", hue="genre", style="genre")
plt.xticks(np.arange(0, 5.1, 0.5))
plt.yticks(np.arange(0, df["reviews"].max() + 1, 5000))
plt.title("Взаємозв'язок між рейтингом користувачів та кількістю відгуків")
plt.show()


# 2
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="genre", y="user_rating", palette="Set2")
plt.yticks(np.arange(0, 5.1, 0.5))
plt.title("Середній рейтинг книг за жанрами")
plt.show()


# 3
avg_price_year = df.groupby("year")["price"].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=avg_price_year, x="year", y="price", marker="o")
plt.xticks(avg_price_year["year"])  # Встановлення міток років
plt.yticks(
    np.arange(0, avg_price_year["price"].max() + 1, 2)
)  # Зміна інтервалу міток на осі Y
plt.title("Зміна середньої ціни книг за роками")
plt.show()
