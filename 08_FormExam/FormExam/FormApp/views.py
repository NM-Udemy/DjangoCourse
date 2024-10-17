from django.shortcuts import render
import os
from . import forms
from .models import Students

def insert_student(request):
    insert_form = forms.StudentsModelForm(request.POST or None,
                                          request.FILES or None)
    if insert_form.is_valid():
        insert_form.save()
    return render(
        request, 'form_app/insert_student.html', context={
            'insert_form': insert_form,
        }
    )
    
def students_list(request):
    students = Students.objects.all()
    return render(
        request, 'form_app/students_list.html', context={
            'students': students,
        }
    )

def update_student(request, id):
    student = Students.objects.get(pk=id)
    old_picture = student.picture
    update_form = forms.StudentsModelForm(
        request.POST or None, request.FILES or None,
        instance=student
    )
    if update_form.is_valid():
        updated_student = update_form.save()
        if old_picture and old_picture.path and old_picture.path != updated_student.picture.path:
            if os.path.isfile(old_picture.path):
                os.remove(old_picture.path)        
    return render(
        request, 'form_app/update_student.html', context={
            'update_form': update_form,
            'student': student,
        }
    )

def delete_student(request, id):
    delete_form = forms.StudentsDeleteForm(
        request.POST or None,
        initial = {
            'id': id
        }
    )
    if delete_form.is_valid():
        student = Students.objects.get(pk=id)
        if student:
            file_path = student.picture.path
            if file_path and os.path.isfile(file_path):
                os.remove(file_path)
            student.delete()
            
    return render(
        request, 'form_app/delete_student.html', context={
            'delete_form': delete_form,
        }
    )
    
def insert_multiple_students(request):
    insert_form = forms.StudentsFormSet(
        request.POST or None, request.FILES or None
    )
    if insert_form.is_valid():
        insert_form.save()
    return render(
        request, 'form_app/insert_multiple_students.html', context={
            'insert_form': insert_form,
        }
    )