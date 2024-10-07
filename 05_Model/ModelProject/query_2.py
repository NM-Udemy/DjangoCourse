import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Students, Person

# IN
ids = [3, 5, 7]
print(Students.objects.filter(pk__in=ids).all())

# contains 部分一致
print(Students.objects.filter(name__contains='三').all())

from datetime import date
# is null
person = Person(
    first_name='Jiro', last_name='Yamada',
    birthday = date(2000,1,1), email='aa@mail.com',
    salary=None, memo='memo taro', web_site='http://taro.com'
)
# person.save()

print(Person.objects.filter(salary__isnull=True).all())

# 取り除く（exclude）
print(Students.objects.exclude(name='太郎').all())
print(Students.objects.exclude(name='太郎').all().query)

# 一部のカラムの取得
print(Students.objects.values('name', 'age').all().query)
students = Students.objects.values('name', 'age').all()
for student in students:
    print(student['name'])

# 並び替え(order_by)
print(Students.objects.values('name').order_by('-name', '-id').all())