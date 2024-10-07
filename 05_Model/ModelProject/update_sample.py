import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Person
from datetime import date
person = Person.objects.get(pk=1)
print(person, person.birthday, person.update_at)

person.birthday = date(2001, 1, 1)
# person.save()

persons = Person.objects.filter(first_name='Jiro').all()

for person in persons:
    person.first_name = person.first_name.lower()
    # person.save()

from datetime import datetime, timezone
Person.objects.filter(last_name='Sato').update(
    web_site='http://sato.jp',
    update_at=datetime.now(timezone.utc),
)
