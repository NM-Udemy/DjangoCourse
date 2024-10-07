import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Person

Person.objects.filter(first_name='Saburo').delete()
Person.objects.filter(first_name='jiro', last_name='Ito').delete()

# 全削除
Person.objects.all().delete()