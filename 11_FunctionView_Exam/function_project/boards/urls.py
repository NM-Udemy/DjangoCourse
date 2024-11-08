from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('create_theme', views.create_theme, name='create_theme'),
    path('list_themes', views.list_themes, name='list_themes'),
    path('edit_theme/<int:pk>', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:pk>', views.delete_theme, name='delete_theme'),
    path('post_comment/<int:theme_id>', views.post_comment, name='post_comment'),
    path('save_comment', views.save_comment, name='save_comment'),
]