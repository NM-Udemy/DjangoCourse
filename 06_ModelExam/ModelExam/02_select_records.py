import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelExam.settings')
from django import setup

setup()

from ModelApp.models import Students, TestResults, Tests, Classes

student = Students.objects.get(pk=1)
for test_result in student.test_results.all(): # type: ignore
    print(
        student.class_fk.name, student.name, test_result.test.name,
        test_result.score,
    )

from django.db.models import Sum, Avg, Max, Min

for class_summary in Classes.objects.values(
    'name', 'students__test_results__test__name'
).annotate(
    sum_score=Sum('students__test_results__score'),
    max_score=Max('students__test_results__score'),
    avg_score=Avg('students__test_results__score'),
    min_score=Min('students__test_results__score'),
):
    print(
        class_summary['name'],
        class_summary['students__test_results__test__name'],
        class_summary['max_score'],
        class_summary['min_score'],
        class_summary['avg_score'],
        class_summary['sum_score'],
    )

print(Classes.objects.values(
    'name', 'students__test_results__test__name'
).annotate(
    sum_score=Sum('students__test_results__score'),
    max_score=Max('students__test_results__score'),
    avg_score=Avg('students__test_results__score'),
    min_score=Min('students__test_results__score'),
).query)