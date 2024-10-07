import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModelProject.settings")
from django import setup

setup()

from ModelApp.models import Students, Schools, Prefectures

student = Students.objects.get(pk=1)
print(type(student), student)
print(student.prefecture.name)
print(student.school.name)
print(student.school.prefecture.name)

school = Schools.objects.get(pk=1)
print(school.name)
print(school.students.all()) # type: ignore
print(school.prefecture.name)

prefecture = Prefectures.objects.get(pk=1)
print(prefecture.schools.first()) # type: ignore

# 1対1
from ModelApp.models import Places, Restaurants

place = Places.objects.get(pk=1)
print(place.restaurant.name) # type: ignore
restaurant = Restaurants.objects.get(pk=1)
print(restaurant.place.name)

# 多対多
from ModelApp.models import Books, Authors

book = Books.objects.get(pk=1)
print(book.authors.all())
author = Authors.objects.get(pk=1)
print(author.books.all()) # type: ignore