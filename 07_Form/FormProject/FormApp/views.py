from django.shortcuts import render
from . import forms
from .models import User, Memo
import os
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'formapp/index.html')

def form_page(request):
    form = forms.UserInfo()
    success_message = ''
    if request.method == 'POST':
        form = forms.UserInfo(request.POST)
        if form.is_valid(): # バリデーション（フィールドのチェック）
            print('バリデーション成功')
            # print(
            #     f"""name: {form.cleaned_data['name']}, 
            #     mail: {form.cleaned_data['mail']},
            #     age: {form.cleaned_data['age']}"""
            # )
            print(form.cleaned_data)
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            mail = form.cleaned_data['mail']
            user = User(
                name=name, age=age, mail=mail
            )
            user.save()
            success_message = f'{name}を登録しました'
            
    form.fields['job'].widget.attrs.update(
        {'class': 'job-class',}
    )
    
    return render(
        request, 'formapp/form_page.html', context={
            'form': form,
            'success_message': success_message
        }
    )

def form_post(request):
    form = forms.PostModelForm()
    if request.method == 'POST':
        form = forms.PostModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(
        request, 'formapp/form_post.html', context={
            'form': form,
        }
    )

def form_set_post(request):
    initial_data = [
        {'title': 'title1', 'memo': 'memo1'},
        {'title': 'title2', 'memo': 'memo2'}
    ]
    formset = forms.MemoFormSet(initial=initial_data)
    if request.method == "POST":
        formset = forms.MemoFormSet(request.POST, initial=initial_data)
        if formset.is_valid():
            for form in formset.forms:
                print(form.cleaned_data)
    return render(
        request, 'formapp/form_set_post.html',
        context={'formset': formset,}
    )

def modelform_set_post(request):
    formset = forms.MemoModelFormSet(request.POST or None,
        # queryset=Memo.objects.order_by('-pk')[:3]
        queryset=Memo.objects.filter(title__contains='new')
    )
    if formset.is_valid():
        formset.save()
    return render(
        request, 'formapp/modelform_set_post.html',
        context={
            'formset': formset,
        }
    )

def upload_sample(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage() # ファイルを保存するオブジェクト
        file_path = os.path.join('upload', upload_file.name)
        print(file_path)
        file = fs.save(file_path, upload_file) # ファイルの保存
        uploaded_file_url = fs.url(file) #　保存したファイルを見るURL
        return render(request, 'formapp/upload_file.html',
                      context={
                          'uploaded_file_url': uploaded_file_url,
                      })
    return render(request, 'formapp/upload_file.html')

def upload_model_form(request):
    form =  forms.ProfileForm(request.POST or None, request.FILES or None)
    profile = None
    if form.is_valid():
        profile = form.save()
    return render(request, 'formapp/upload_model_form.html', context={
        'form': form, 'profile': profile,
    })