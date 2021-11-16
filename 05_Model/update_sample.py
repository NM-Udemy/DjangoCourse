import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Person
from django.utils import timezone
import pytz

person = Person.objects.get(id=1)
print(person)
person.birthday = '2001-01-01'
person.update_at = timezone.datetime.now(pytz.timezone('Asia/Tokyo'))
# person.save()

persons = Person.objects.filter(first_name='Taro').all()
for person in persons:
    person.first_name = person.first_name.lower()
    person.update_at = timezone.datetime.now(pytz.timezone('Asia/Tokyo'))
    # person.save()
Person.objects.filter(first_name='Saburo').update(
    web_site='http://sample.jp',
    update_at=timezone.datetime.now(pytz.timezone('Asia/Tokyo'))
)