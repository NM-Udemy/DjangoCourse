from django.urls import path
from .views import (
    IndexView, HomeView, BookDetailView,
    BookListView, BookCreateView, BookUpdateView,
    BookDeleteView, BookFormView, BookRedirectView,
    delete_picture,
)
# from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView

app_name = 'store'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/<name>', HomeView.as_view(), name='home'),
    path('detail_book/<int:pk>', BookDetailView.as_view(), name='detail_book'),
    path('list_books/', BookListView.as_view(), name='list_books'),
    path('list_books/<name>', BookListView.as_view(), name='list_books'),
    path('add_book/', BookCreateView.as_view(), name='add_book'),
    path('edit_book/<int:pk>', BookUpdateView.as_view(), name='edit_book'),
    path('delete_book/<int:pk>', BookDeleteView.as_view(), name='delete_book'),
    path('book_form/', BookFormView.as_view(), name='book_form'),
    path('google/', RedirectView.as_view(url='https://google.co.jp')),
    path('book_redirect_view/', BookRedirectView.as_view(), name='book_redirect_view'),
    path('book_redirect_view/<int:pk>', BookRedirectView.as_view(), name='book_redirect_view'),
    path('delete_picture/<int:pk>', delete_picture, name='delete_picture'),
]