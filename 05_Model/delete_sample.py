import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Person

Person.objects.filter(first_name='Saburo').delete()

Person.objects.filter(first_name='taro', birthday='2001-01-01').delete()

#全件削除
Person.objects.all().delete()
