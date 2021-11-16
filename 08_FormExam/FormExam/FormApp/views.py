from django.shortcuts import render
from . import forms
from .models import Students
from django.core.files.storage import FileSystemStorage
import os
from django.forms import modelformset_factory
# Create your views here.


def insert_student(request):
    insert_form = forms.StudentInsertForm(request.POST or None, request.FILES or None)
    if insert_form.is_valid():
        insert_form.save()
        insert_form = forms.StudentInsertForm()
    return render(
        request, 'form_app/insert_student.html', context={
            'insert_form': insert_form
        }
    )

def students_list(request):
    students = Students.objects.all()
    return render(
        request, 'form_app/students_list.html', context={
            'students': students
        }
    )

def update_student(request, id):
    student = Students.objects.get(id=id)
    update_form = forms.StudentUpdateForm(
        initial = {
            'name': student.name, 'age': student.age, 'grade': student.grade, 'picture': student.picture
        }
    )
    if request.method == 'POST':
        update_form = forms.StudentUpdateForm(request.POST or None, request.FILES or None)
        if update_form.is_valid():
            student.name = update_form.cleaned_data['name']
            student.age = update_form.cleaned_data['age']
            student.grade = update_form.cleaned_data['grade']
            picture = update_form.cleaned_data['picture']
            if picture:
                fs = FileSystemStorage()
                file_name = fs.save(os.path.join('student', picture.name), picture)
                student.picture = file_name
            student.save()
    return render(
        request, 'form_app/update_student.html', context={
            'update_form': update_form,
            'student': student
        }
    )


def delete_student(request, id):
    delete_form = forms.StudentDeleteForm(
        initial={
            'id': id
        }
    )
    if request.method == 'POST':
        delete_form = forms.StudentDeleteForm(request.POST or None)
        if delete_form.is_valid():
            Students.objects.get(id=delete_form.cleaned_data['id']).delete()
    return render(
        request, 'form_app/delete_student.html', context={
            'delete_form': delete_form
        }
    )    

def insert_multiple_students(request):
    StudentFormSet = modelformset_factory(Students, fields='__all__', extra=3)
    insert_form = StudentFormSet(request.POST or None, request.FILES or None)
    if insert_form.is_valid():
        insert_form.save()
    return render(
        request, 'form_app/insert_multiple_students.html', context={
            'insert_form': insert_form
        }
    )