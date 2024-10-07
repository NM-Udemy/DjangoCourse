import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Students

# 全件取得
print(Students.objects.all())

# 頭の5件取得
print(Students.objects.all()[:5])

# 5件目よりあと
print(Students.objects.all()[5:])

# 6~8件目
print(Students.objects.all()[5:8])
print(Students.objects.all()[5:8].query)

# 1番目の1件
print(Students.objects.first())

# 等しいものだけ絞り込む
print(Students.objects.filter(name='太郎').all())
print(Students.objects.filter(age=17).all())

# AND条件
print(Students.objects.filter(name='太郎', pk__gt=9).all())
print(Students.objects.filter(name='太郎', pk__gt=9).all().query)
print(Students.objects.filter(
    name='次郎', pk__gte=5, pk__lte=12).all()
)

# 前方一致、後方一致
print(Students.objects.filter(name__startswith='太').all())
print(Students.objects.filter(name__endswith='郎').all())

# or
from django.db.models import Q
print(Students.objects.filter(Q(name='太郎') | Q(pk__gt=10)).all())