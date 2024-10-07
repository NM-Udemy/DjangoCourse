import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModelProject.settings')
from django import setup
setup()

from ModelApp.models import Books, Authors

def insert_books():
    book1 = Books(name='Book1')
    book2 = Books(name='Book2')
    book3 = Books(name='Book3')
    book1.save()
    book2.save()
    book3.save()
    
def insert_authors():
    author1 = Authors(name='Author1')
    author2 = Authors(name='Author2')
    author3 = Authors(name='Author3')
    author1.save()
    author2.save()
    author3.save()

# insert_books()
# insert_authors()

book1 = Books.objects.get(pk=1)
book3 = Books.objects.get(pk=3)

author1 = Authors.objects.get(pk=1)
author2 = Authors.objects.get(pk=2)
author3 = Authors.objects.get(pk=3)

book1.authors.add(author1, author2)
# print(book1.authors.all()[0].name)

book3.authors.add(author3)