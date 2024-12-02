from django import forms
from .models import Books, Pictures

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Books
        fields = ['name', 'description', 'price']
        labels = {
            'name': '書籍名',
            'description': '説明',
            'price': '価格'
        }


class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ['picture',]

