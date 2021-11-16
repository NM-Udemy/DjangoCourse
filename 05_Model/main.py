import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()
from ModelApp.models import Person

p = Person(
    first_name='Taro', last_name='Sato',
    birthday='2000-01-01', email='aa@mail.com',
    salary=10000, memo='memo taro', web_site='http://www.google'
)
p = Person(
    first_name='Taro', last_name='Sato',
    birthday='2000-01-01', email='aa@mail.com',
    salary=None, memo='memo taro', web_site='http://www.google'
)
p = Person(
    first_name='Taro', last_name='Sato',
    birthday='2000-01-01', email='aa@mail.com',
    salary=None, memo='memo taro', web_site=''
)

# p.save()

# classmethod create
# Person.objects.create(
#     first_name='Jiro', last_name='Ito',
#     email='bb@mail.com',
#     salary = 20000, memo='class method 実行', web_site=None
# )
# get_or_create(取得 or 作成)

obj, created = Person.objects.get_or_create(
    first_name='Saburo', last_name='Ito',
    email='bb@mail.com',
    salary = 40000, memo='class method 実行', web_site=None
)

print(obj)
print(created)
