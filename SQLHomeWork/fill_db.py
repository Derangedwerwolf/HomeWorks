from datetime import date, datetime, timedelta
import faker
import sqlite3
from random import randint


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    disciplines = [
        "Вища математика",
        "Хімія",
        "Економіка підприємства",
        "Обчислювальна математика",
        "Історія України",
        "Теоретична механіка",
        "Менеджмент організацій",
        "Системне програмування",
    ]

    groups = ["ВВ1", "ДД33", "АА5"]

    fake = faker.Faker("uk-UA")
    conn = sqlite3.connect("university.db")
    cur = conn.cursor()

    number_of_teachers = 5
    number_of_students = 50

    def seed_teachers():
        teachers = []

        for _ in range(number_of_teachers):
            teachers.append(fake.name())

        sql_teachers = "INSERT INTO teachers(fullname) VALUES (?)"

        cur.executemany(
            sql_teachers,
            zip(
                teachers,
            ),
        )

    def seed_disciplines():
        sql_disc = "INSERT INTO disciplines(name, teacher_id) VALUES (?, ?)"
        cur.executemany(
            sql_disc,
            zip(
                disciplines,
                iter(randint(1, number_of_teachers) for _ in range(len(disciplines))),
            ),
        )

    def seed_groups():
        sql_groups = "INSERT INTO groups(name) VALUES (?)"
        cur.executemany(
            sql_groups,
            zip(
                groups,
            ),
        )

    def seed_students():
        students = []

        for _ in range(number_of_students):
            students.append(fake.name())

        sql_students = "INSERT INTO students(fullname, group_id) VALUES (?,?)"

        cur.executemany(
            sql_students,
            zip(students, iter(randint(1, len(groups)) for _ in range(len(students)))),
        )

    def seed_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)

        grades = []

        for d in d_range:
            r_disc = randint(1, len(disciplines))
            r_students = [randint(1, number_of_students) for _ in range(3)]

            for student in r_students:
                grades.append((student, r_disc, d.date(), randint(1, 12)))

        sql_ratings = "INSERT INTO grades(student_id, discipline_id, date_of, grade) VALUES (?, ?, ?, ?)"
        cur.executemany(sql_ratings, grades)

    try:
        seed_teachers()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grades()
        conn.commit()

    except sqlite3.IntegrityError as err:
        print(err)

    finally:
        conn.close()


# if __name__ == "__main__":
#     create_db("university.sql")
#     fill_data()
