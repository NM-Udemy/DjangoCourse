import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelExam.settings')
from django import setup

setup()

from ModelApp.models import Students, TestResults, Tests, Classes
from random import randint

class_names = ['Class' + c for c in 'ABCDEFGHIJ']
student_names = ['Student' + c for c in 'ABCDEFGHIJ']
test_names = ['数学', '英語', '国語']

# テストの挿入
inserted_tests = []
for test_name in test_names:
    test = Tests(name=test_name)
    test.save()
    inserted_tests.append(test)
    

for class_name in class_names:
    inserted_class = Classes(
        name=class_name
    )
    inserted_class.save() #  クラス挿入
    for student_name in student_names:
        name = class_name + ' ' + student_name # ClassA StudentA, ClassC StudentE
        student = Students(
            name=name,
            class_fk=inserted_class,
            grade=1,
        )
        student.save() # Student挿入
        for inserted_test in inserted_tests:
            test_result = TestResults(
                student=student,
                test=inserted_test,
                score=randint(50, 100),
            )
            test_result.save() # TestResults挿入