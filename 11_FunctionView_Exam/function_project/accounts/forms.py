from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='パスワード再入力', widget=forms.PasswordInput()
    )
    
    class Meta():
        model = User
        fields = ('username', 'age', 'email', 'password')
        labels = {
            'username': '名前',
            'age': '年齢',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }
        widgets = {
            'age': forms.NumberInput(attrs={
                'min': 0
            }),
            'password': forms.PasswordInput()
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しません')
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            self.add_error('password', e)
        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserActivateForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())

class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'age', 'email', 'picture')
        labels = {
            'username': '名前',
            'age': '年齢',
            'email': 'メールアドレス',
            'picture': '写真',
        }
        widgets = {
            'age': forms.NumberInput(attrs={
                'min': '0'
            })
        }
        required = {
            'picture': False,
        }
        
class PasswordChangeForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='パスワード再設定', widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ('password',)
        labels = {
            'password': 'パスワード',
        }
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            self.add_error('password', 'パスワードが一致しません')
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            self.add_error('password', e)
        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user