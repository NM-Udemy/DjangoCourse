import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelExam.settings')
from django import setup
setup()

from ModelApp.models import Students, Classes

student = Students.objects.get(pk=1)
for test_result in student.testresults_set.all():
    print(student.class_fk.name, student.name, test_result.test.name, test_result.score)

from django.db.models import Sum, Avg, Max, Min

# GROUP By クラス名, テスト名
for class_summary in Classes.objects.values('name', 'students__testresults__test__name').annotate(
    max_score = Max('students__testresults__score'),
    min_score = Min('students__testresults__score'),
    avg_score = Avg('students__testresults__score'),
    sum_score = Sum('students__testresults__score'),
):
    print(
        class_summary['name'],
        class_summary['students__testresults__test__name'],
        class_summary['max_score'],
        class_summary['min_score'],
        class_summary['avg_score'],
        class_summary['sum_score']
    )

print(Classes.objects.values('name', 'students__testresults__test__name').annotate(
    max_score = Max('students__testresults__score'),
    min_score = Min('students__testresults__score'),
    avg_score = Avg('students__testresults__score'),
    sum_score = Sum('students__testresults__score'),
).query)