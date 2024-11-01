from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# ユーザー作成用のForm
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（確認）', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        return user

# ユーザー編集用のForm
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='パスワード')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser')
    
    def clean_password(self):
        return self.instance.password
