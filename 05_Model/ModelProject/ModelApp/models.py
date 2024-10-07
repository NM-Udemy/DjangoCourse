from django.db import models
from datetime import date, datetime


class BaseMeta(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Person(BaseMeta):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(default=date(1900, 1, 1))
    email = models.EmailField(db_index=True)
    salary = models.FloatField(null=True)
    memo = models.TextField()
    web_site = models.URLField(null=True)
    
    class Meta:
        db_table = 'person'
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]
        ordering = ['salary']
        
    def __str__(self):
        return f"{self.pk}: {self.first_name}, {self.last_name}"

class StudentsManager(models.Manager):
    
    def filter_by_name(self, name):
        return self.filter(name=name)


class Students(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    major = models.CharField(max_length=20)
    school = models.ForeignKey(
        'Schools', on_delete=models.RESTRICT, related_name='students'
    )
    prefecture = models.ForeignKey(
        'Prefectures', on_delete=models.CASCADE,
    )
    
    objects: StudentsManager = StudentsManager()
    
    class Meta:
        db_table = 'students'
        
    def __str__(self):
        return f'{self.pk}, {self.name}, {self.age}'
    
class Schools(models.Model):
    name = models.CharField(max_length=20)
    prefecture = models.ForeignKey(
        'Prefectures', on_delete=models.CASCADE, related_name='schools'
    )
    
    class Meta:
        db_table = 'schools'
    

class Prefectures(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'prefectures'

class Places(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    
    class Meta:
        db_table = 'places'

class Restaurants(models.Model):
    place = models.OneToOneField(
        Places,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='restaurant'
    )
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'restaurants'

class Authors(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'authors'

class Books(models.Model):
    name = models.CharField(max_length=50)
    authors = models.ManyToManyField(Authors,
                                     related_name='books')
    
    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.name
    