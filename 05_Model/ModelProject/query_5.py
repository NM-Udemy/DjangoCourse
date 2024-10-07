import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Students

queryset = Students.objects.all()
queryset = queryset.filter(name='太郎')
# queryset = queryset.filter(pk=1)
filter_value = input()
if filter_value:
    queryset = queryset.order_by(filter_value)
queryset = queryset[:2]
print(list(queryset), type(queryset))

print(Students.objects.filter_by_name('次郎'))
