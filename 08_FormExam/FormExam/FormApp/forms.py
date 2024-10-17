from .models import Students
from django import forms

class StudentsModelForm(forms.ModelForm):
    
    class Meta:
        model = Students
        fields = '__all__'
        labels = {
            'name': '名前',
            'age': '年齢',
            'grade': '学年',
            'picture': 'ファイルアップロード'
        }

class StudentsDeleteForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)

StudentsFormSet = forms.modelformset_factory(Students, fields='__all__', extra=3)