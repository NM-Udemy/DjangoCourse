import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Students, Schools, Prefectures

prefectures = ['東京', '大阪']
schools = ['東高校', '西高校', '北高校', '南高校']
students = ['太郎', '次郎', '三郎']

def insert_records():
    for prefecture_name in prefectures:
        prefecture = Prefectures(
            name=prefecture_name,
        )
        prefecture.save()
        for school_name in schools:
            school = Schools(
                name=school_name,
                prefecture=prefecture,
            )
            school.save()
            for student_name in students:
                student = Students(
                    name=student_name, age=17,
                    major='物理', prefecture=prefecture, school=school
                )
                student.save()

def select_students():
    students = Students.objects.all()
    for student in students:
        if student.school:
            print(
                student.pk, student.name,
                student.school.pk, student.school.name,
                student.school.prefecture.pk, student.school.prefecture.name 
            )
        else:
            print(student.pk, student.name)
# insert_records()
# select_students()
# Students.objects.filter(id=1).delete()
# Schools.objects.filter(id=1).delete()
Prefectures.objects.filter(id=1).delete()