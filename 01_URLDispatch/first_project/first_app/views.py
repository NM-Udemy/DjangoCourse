from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Good Bye</h1>')

def user_page(request, user_name):
    return HttpResponse(f'<h1>{user_name} Page</h1>')

def number_page(request, user_name, number):
    return HttpResponse(f'<h1>{user_name} page number = {number}</h1>')