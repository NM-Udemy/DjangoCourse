from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=255)
    password1 = forms.CharField(
        label='パスワード', max_length=50, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='パスワード(再)', max_length=50, widget=forms.PasswordInput
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('パスワードが一致しません')
        return cleaned_data

class RequestPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput()
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('このメールアドレスのユーザーは存在しません')
        return email
    

class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='新しいパスワード（確認）',
        widget=forms.PasswordInput,
    )
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('パスワードが一致しません')
        else:
            raise ValidationError('パスワードを設定してください')
        return cleaned_data