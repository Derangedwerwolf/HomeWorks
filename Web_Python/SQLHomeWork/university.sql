CREATE TABLE IF NOT EXISTS [groups] (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name STRING UNIQUE
);

CREATE TABLE IF NOT EXISTS [teachers] (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fullname STRING
);

CREATE TABLE IF NOT EXISTS [students] (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fullname STRING,
    group_id REFERENCES [groups] (id)
);

CREATE TABLE IF NOT EXISTS [disciplines] (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name STRING,
    teacher_id REFERENCES [teachers] (id)
);

CREATE TABLE IF NOT EXISTS [grades] (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    discipline_id REFERENCES [disciplines] (id),
    student_id REFERENCES [students] (id),
    grade INTEGER,
    date_of DATE
);