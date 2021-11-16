from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password再入力', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    website = forms.URLField(required=False)
    picture = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'website', 'picture')
    
    def clean_password(self):
        # すでに登録されているパスワードを返す
        return self.initial['password']
