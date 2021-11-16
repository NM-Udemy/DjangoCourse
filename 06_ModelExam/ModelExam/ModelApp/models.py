from django.db import models


class Classes(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'classes'


class Students(models.Model):
    name = models.CharField(max_length=50)
    grade = models.IntegerField()
    class_fk = models.ForeignKey(
        'Classes',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'students'


class Tests(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tests'


class TestResults(models.Model):
    score = models.IntegerField()
    student = models.ForeignKey(
        'Students',
        on_delete=models.CASCADE,
    )
    test = models.ForeignKey(
        'Tests',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'test_results'
