from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from django.core import validators
from .models import Post, Memo, Profile
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

def check_name(value):
    if value == 'あああああ':
        raise ValidationError('その名前は登録できません')

class UserInfo(forms.Form):
    name = forms.CharField(label='名前',
                           min_length=5, max_length=10,
        validators=[
            check_name,
        ]
    )
    age = forms.IntegerField(label='年齢',
        validators=[validators.MinValueValidator(
            20, message='20以上にしてください'
        )],
    )
    mail = forms.EmailField(label='メールアドレス',
        widget=forms.TextInput(attrs={
            'class': 'mail-class',
            'placeholder': 'sample@mail.com'
        })
    )
    verify_mail = forms.EmailField(label='メールアドレス再入力',
        widget=forms.TextInput(attrs={'placeholder': 'sample@mail.com'})
    )
    verify_mail.widget.attrs.update({
        'class': 'mail-class',
    })
    is_married = forms.BooleanField(initial=True)
    birthday = forms.DateField(initial=date(1990,1,1))
    salary = forms.DecimalField()
    job = forms.ChoiceField(choices=(
        (1, '正社員'),
        (2, '自営業'),
        (3, '学生'),
        (4, '無職'),
    ), widget=forms.RadioSelect)
    hobbies = forms.MultipleChoiceField(choices=(
        (1, 'スポーツ'),
        (2, '読書'),
        (3, '映画鑑賞'),
        (4, 'その他'),
    ), widget=forms.CheckboxSelectMultiple)
    homepage = forms.URLField(required=False)
    memo = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job'].widget.attrs.update({'id': 'job'})
        self.fields['hobbies'].widget.attrs.update({'class': 'hobbies_class'})
    
    def clean_homepage(self):
        homepage = self.cleaned_data.get('homepage', '')
        if not homepage.startswith('https'):
            raise ValidationError('httpsで始めてください')
        return homepage

    # Override
    def clean(self):
        cleaned_data = super().clean()
        mail = cleaned_data.get('mail', '')
        verify_mail = cleaned_data.get('verify_mail', '')
        if mail != verify_mail:
            raise ValidationError('メールアドレスが一致しません')
        return cleaned_data

class PostModelForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['name', 'title']
        # exclude = ['title']
        labels = {
            'name': '名前',
            'title': 'タイトル',
            'memo': 'メモ',
        }
        widgets = {
            'memo': forms.Textarea(
                attrs={'rows': 30, 'cols': 20}
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'new_name_class',
        })
        
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if name == 'ああああ':
            raise ValidationError('その名前は登録できません')
        return name
        
    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title == 'ああああ':
            raise ValidationError('そのタイトルは登録できません')
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '')
        memo = cleaned_data.get('memo', '')
        post = Post.objects.filter(title=title, memo=memo).first()
        if post:
            raise ValidationError('そのtitleとmemoは存在します')
        return cleaned_data
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = instance.name.upper()
        if commit:
            instance.save()
        return instance

class MemoForm(forms.Form):
    title = forms.CharField(label='タイトル')
    memo = forms.CharField(label='メモ')
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'title':
            raise ValidationError('そのタイトルは入れられません')
        return title

class CustomMemoFormSet(forms.BaseFormSet):
    
    default_error_messages = {
        "missing_management_form": _(
            "ManagementForm data is missing or has been tampered with. Missing fields: "
            "%(field_names)s. You may need to file a bug report if the issue persists."
        ),
        "too_many_forms": ngettext_lazy(
            "%(num)d個以下のフォームを送信してください",
            "%(num)d個以下のフォームを送信してください",
            "num",
        ),
        "too_few_forms": ngettext_lazy(
            "Please submit at least %(num)d form.",
            "Please submit at least %(num)d forms.",
            "num",
        ),
    }
    
    def clean(self):
        super().clean()
        titles = []
        for form in self.forms:
            if form.cleaned_data['title'] not in titles:
                titles.append(form.cleaned_data['title'])
            else:
                raise ValidationError('同じタイトルを入れないでください')

MemoFormSet = forms.formset_factory(MemoForm, formset=CustomMemoFormSet,
                                    extra=3, max_num=5, validate_max=True)

class MemoModelForm(forms.ModelForm):
    
    class Meta:
        model = Memo
        fields = '__all__'
        labels = {
            'title': 'タイトル',
            'memo': 'メモ',
        }


class CustomMemoModelFormSet(forms.BaseModelFormSet):
    
    default_error_messages = {
        "missing_management_form": _(
            "ManagementForm data is missing or has been tampered with. Missing fields: "
            "%(field_names)s. You may need to file a bug report if the issue persists."
        ),
        "too_many_forms": ngettext_lazy(
            "%(num)d個以下のフォームを送信してください",
            "%(num)d個以下のフォームを送信してください",
            "num",
        ),
        "too_few_forms": ngettext_lazy(
            "Please submit at least %(num)d form.",
            "Please submit at least %(num)d forms.",
            "num",
        ),
    }
    
    def clean(self):
        super().clean()
        titles = []
        for form in self.forms:
            if form.cleaned_data['title'] not in titles:
                titles.append(form.cleaned_data['title'])
            else:
                raise ValidationError('同じタイトルを入れないでください')


MemoModelFormSet = forms.modelformset_factory(
    Memo, form=MemoModelForm, formset=CustomMemoModelFormSet,
    extra=3, max_num=5, validate_max=True,
)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
