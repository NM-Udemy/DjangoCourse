from django import forms
from django.core import validators

from .models import Post, ModelSetPost, User

def check_name(value):
    if value == 'あああああ':
        raise validators.ValidationError('そのなまえは登録できない')

class UserInfo(forms.Form):
    name = forms.CharField(label='名前', min_length=5, max_length=10, validators=[check_name])
    age = forms.IntegerField(label='年齢', validators=[validators.MinValueValidator(20, message='20以上にしましょう')])
    mail = forms.EmailField(
        label='メールアドレス',
        widget=forms.TextInput(attrs={'class': 'mail-class', 'placeholder': 'sample@mail.com'})
    )
    verify_mail = forms.EmailField(
        label='メールアドレス再入力',
        widget=forms.TextInput(attrs={'class': 'mail-class', 'placeholder': 'sample@mail.com'})
    )
    is_married = forms.BooleanField(initial=True)
    birtyday = forms.DateField(initial='1990-01-01')
    salary = forms.DecimalField()
    job = forms.ChoiceField(choices=(
        (1, '正社員'),
        (2, '自営業'),
        (3, '学生'),
        (4, '無職')
    ), widget=forms.RadioSelect)
    hobbies = forms.MultipleChoiceField(choices=(
        (1, 'スポーツ'),
        (2, '読書'),
        (3, '映画鑑賞'),
        (4, 'その他')
    ))
    homepage = forms.URLField(required=False)
    memo = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs['id'] = 'id_job'
        self.fields['hobbies'].widget.attrs['class'] = 'hobbies_class'

    def clean_homepage(self):
        homepage = self.cleaned_data['homepage']
        if not homepage.startswith('https'):
            raise forms.ValidationError('ホームページのURLはhttpsのみ！！')
        return homepage
    
    def clean(self):
        cleaned_data = super().clean()
        mail = cleaned_data['mail']
        verify_mail = cleaned_data['verify_mail']
        if mail != verify_mail:
            raise forms.ValidationError('メールアドレスが一致しません！！')


class BaseForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        print(f'Form: {self.__class__.__name__}実行')
        return super(BaseForm, self).save(*args, **kwargs)


class PostModelForm(BaseForm):
    name = forms.CharField(label='名前')
    title = forms.CharField(label='タイトル')
    memo = forms.CharField(
        label='メモ', widget=forms.Textarea(attrs={'rows': 30, 'cols': 20})
    )

    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['name', 'title']
        # exclude =['title']

    def save(self, *args, **kwargs):
        obj = super(PostModelForm, self).save(commit=False, *args, **kwargs)
        obj.name = obj.name.upper()
        print(type(obj))
        print('save実行')
        obj.save()
        return obj

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == 'ああああ':
            raise validators.ValidationError('名前が登録できません')
        return name

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'ああああ':
            raise validators.ValidationError('そのタイトルは登録できません')
        return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        is_exists = Post.objects.filter(title=title).first()
        if is_exists:
            raise validators.ValidationError('そのタイトルはすでの存在します')
    
class FormSetPost(forms.Form):
    title = forms.CharField(label='タイトル')
    memo = forms.CharField(label='メモ')


class ModelFormSetPost(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    memo = forms.CharField(label='メモ')

    class Meta:
        model = ModelSetPost
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'