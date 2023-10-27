from sqlalchemy import func, select, desc, and_

from source.models import Teacher, Student, Discipline, Grade, Group
from source.db import session
from pprint import pprint
import sys


help_message = """
Виберіть який запит ви хочете виконати?
0 -- Вихід
1 -- Знайти 5 студентів з найбільшим середнім балом по всім предметам
2 -- Знайти студента з найбільшим середнім балом з дисципліни. (Перша дисципліна)
3 -- Знайти середній балл в групі по дисципліні. (Друга дисципліна)
4 -- Знайти середній бал на потоці (по всій таблиці grades)
5 -- Які курси веде викладач. (Перший id=1)
6 -- Список студентів в групі. (Перша група)
7 -- Оцінки студентів в окремій групі за конкретною дисципліною.
8 -- Знайти середній балл, який ставить викладач по своїм дисциплінам. (Перший викладач)
9 -- Знайти список курсів, які відвідує студент.
10 -- Знайти список курсів, які конкретному студенту веде конкретний викладач.
11 -- Середній балл, який конкретний викладач ставит конкретному студенту.
12 -- Оцінки студентів в групі по дисципліні на останньому занятті.
"""


def select_one():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.    
    """
    
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avrg_grade'))\
            .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avrg_grade')).limit(5).all()
    # for row in result:
    #     pprint(row)
    return result


def select_two():
    """
    Знайти студента з найбільшим середнім балом з дисципліни.
    """
    
    result = session.query(
                        Discipline.name,
                        Student.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade).join(Student).join(Discipline)\
                        .filter(Discipline.id == 5)\
                        .group_by(Student.id, Discipline.name).order_by(desc('avg_grade')).limit(1).first()
    return result


def select_three():
    """
    Cредний балл в группе по одному предмету.
    """
    
    result = session.execute(select(
                        Discipline.name,
                        Group.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade).join(Student).join(Discipline)\
                        .filter(Discipline.id == 2)\
                        .group_by(Group.name,Discipline.name).order_by(desc('avg_grade'))).all()
    return result
    
def select_four():
    """
    Знайти середній бал на потоці (по всій таблиці grades)
    """
    
    return session.execute(select(func.round(func.avg(Grade.grade), 2).label('avg_grade'))).one()
    return result


def select_five():
    """
    які курси читає певний викладач.
    """
    
    result = session.execute(select(Teacher.fullname, Discipline.name).select_from(Teacher).join(Discipline).filter(Teacher.id == 5)).all()
    return result


def select_six():
    """
    список студентів у певній групі.
    """

    result = session.execute(select(Student.id, Student.fullname, Group.name)\
                        .select_from(Student).join(Group).order_by(Student.id).filter(Group.id == 1)).all()
    return result


def select_seven():
    """
    оцінки студентів у окремій групі з певного предмета.
    """
    
    result = session.execute(select(Discipline.name, Group.name, Student.fullname, Grade.date_of, Grade.grade)\
                        .select_from(Grade).join(Student).join(Discipline).join(Group)\
                        .filter(and_(Discipline.id == 2, Group.id == 1))\
                        .group_by( Group.name, Student.fullname, Grade.date_of, Grade.grade)\
                        .order_by(Student.fullname)).all()
                        
    return result


def select_eight():
    """
    середній бал, який ставить певний викладач зі своїх предметів
    """
    
    result = session.execute(select(Teacher.fullname, Discipline.name, 
                                    func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                                    .select_from(Grade).join(Discipline).join(Teacher)\
                                    .filter(Teacher.id == 5).group_by(Teacher.fullname, Discipline.name)).all()
    return result


def select_nine():
    """
    список курсів, які відвідує студент.
    """

    result = session.execute(select(Student.fullname, Discipline.name).select_from(Grade).join(Student).join(Discipline)\
                        .filter(Grade.student_id == 1).group_by(Discipline.name)).all()
    return result
    

def select_ten():
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    
    result = session.execute(select(Student.fullname, Teacher.fullname, Discipline.name)\
                        .select_from(Grade).join(Student).join(Discipline).join(Teacher)\
                        .filter(and_(Grade.student_id == 2), (Teacher.id == 4))\
                        .group_by(Discipline.name, Student.fullname, Teacher.fullname)).all()

    return result 
    

def select_eleven():
    """
    Середній бал, який певний викладач ставить певному студентові.
    """
    
    result = session.execute(select(Student.fullname, Teacher.fullname,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade).join(Student).join(Discipline).join(Teacher)\
                        .filter(and_(Grade.student_id == 4), (Teacher.id == 3))
                        .group_by(Student.fullname, Teacher.fullname)).all()
    return result


def select_twelve():
    """
    Оцінки студентів у певній групі з певного предмета на останньому занятті.
    """
    sub_result = session.execute(select(func.max(Grade.date_of)).select_from(Grade)\
                        .join(Student).join(Group).filter(and_(Grade.discipline_id == 8), 
                        (Group.id == 1))).first()
    
    #print(sub_result[0])
    
    result = session.execute(select(Discipline.name, Group.name, Student.fullname, Grade.date_of, Grade.grade)\
                        .select_from(Grade).join(Student).join(Discipline).join(Group)\
                        .filter(and_(Discipline.id == 8), (Group.id == 1), 
                        (Grade.date_of == sub_result[0]) ) ).all()
    return result


COMMANDS_LIST = {
    '1' : select_one,
    '2' : select_two,
    '3' : select_three,
    '4': select_four,
    '5': select_five,
    '6' : select_six,
    '7' : select_seven,
    '8' : select_eight,
    '9' : select_nine,
    '10' : select_ten,
    '11': select_eleven,
    '12' : select_twelve,
}



def main():
    print(help_message)
    while True:
        task = int(input("Виберіть номер запиту: "))

        if task == 0:
            sys.exit()

        result = COMMANDS_LIST[str(task)]()
        pprint(result)


if __name__ == "__main__":
    try:
        exit(main())
        #select_one()
    except KeyboardInterrupt:
        exit()