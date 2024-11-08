from django import forms
from .models import Theme, Comment

class CreateThemeForm(forms.ModelForm):
    
    class Meta:
        model = Theme
        fields = ('title',)
        labels = {
            'title': 'タイトル',
        }
        
class DeleteThemeForm(forms.Form):
    pass

class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(
                attrs={'rows': 5, 'cols': 60},
            )
        }
        labels = {
            'comment': '',
        }
