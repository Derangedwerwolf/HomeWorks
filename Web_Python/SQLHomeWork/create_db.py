import sqlite3
import os

from fill_db import fill_data


def create_db(path):
    if not os.path.exists(f'{os.path.basename(path).split(".")[0]}.db'):
        with open(path, "r") as f:
            sql = f.read()

        with sqlite3.connect(f'{os.path.basename(path).split(".")[0]}.db') as con:
            cur = con.cursor()
            cur.executescript(sql)
            cur.commit()


if __name__ == "__main__":
    path = "university.sql"
    create_db(path)
    fill_data()
