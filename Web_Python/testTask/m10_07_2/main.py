from datetime import datetime

from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import and_

from database.db import session
from database.models import Teacher, Student, ContactPerson, TeacherStudent


def get_students():
    students = session.query(Student).join(Student.teachers).all()
    for st in students:
        print(vars(st))
        print(f"{[t.fullname for t in st.teachers]}")
        

