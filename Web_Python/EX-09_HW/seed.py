from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from source.models import Teacher, Student, Discipline, Grade, Group
from source.db import session


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result
 

def feed_data():
    disciplines = [
        "Авіаційна та ракетно-космічна техніка",
        "Аналіз даних",
        "Алгоритми та програми",
        "Аналітичні та обчислювальні основи",
        "Вища математика",
        "Структурне програмування",
        "Теоретична механіка",
        "Програмування"
    ]
    
    groups = ["ВВ1", "ДД33", "АА5"]
    
    fake = faker.Faker("uk-UA")
    
    number_of_teachers = 5
    number_of_students = 50
    
    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()
    
    def seed_disciplines():
        teachers_id = session.scalars(select(Teacher.id)).all()
        
        for disc in disciplines:
            session.add(Discipline(name=disc, teacher_id=choice(teachers_id)))
        session.commit()
        
    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()
        
    def seed_students():
        groups_id = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(fullname=fake.name(), group_id=choice(groups_id))
            session.add(student)
        session.commit()
        
    def seed_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        
        disciplines_id = session.scalars(select(Discipline.id)).all()
        students_id = session.scalars(select(Discipline.id)).all()
        
        for d in d_range:
            random_id_discipline = choice(disciplines_id)
            random_id_student = [choice(students_id) for _ in range(4)]
            
            for student_id in random_id_student:
                grade = Grade(
                    grade=randint(1, 12), 
                    date_of=d, 
                    student_id=student_id,
                    discipline_id=random_id_discipline
                )
                session.add(grade)
        session.commit()
        
    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()
        

if __name__ == "__main__":
    feed_data()        