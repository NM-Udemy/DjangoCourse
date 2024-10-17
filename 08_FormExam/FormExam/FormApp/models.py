from django.db import models


class Students(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    picture = models.FileField(upload_to='student/')
    
    class Meta:
        db_table = 'students'
