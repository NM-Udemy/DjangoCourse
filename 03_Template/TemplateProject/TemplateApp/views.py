from django.shortcuts import render

# Create your views here.
def index(request):
    val = 'Good Bye'
    return render(request, 'TemplateApp/index.html', context={'value': val})

def home(request, first_name, last_name):
    my_name = f'{first_name} {last_name}'
    favourite_fruits = ['Apple', 'Grape', 'Lemon']
    my_info = {
        'name': 'Taro',
        'age': 18
    }
    status = 20
    return render(request, 'home.html', context={
        'my_name': my_name,
        'favourite_fruits': favourite_fruits,
        'my_info': my_info,
        'status': status
    })

def sample1(request):
    return render(request, 'sample1.html')

def sample2(request):
    return render(request, 'sample2.html')

def sample(request):
    name = 'ichiro yamada'
    height = 175.5
    weight = 72
    bmi = weight / (height / 100)**2
    page_url = 'ホームページ: https://www.google.com'
    favourite_fruits = [
        'Apple', 'Grape', 'Lemon'
    ]
    msg = """hello
    my name is
    ichiro
    """
    msg2 = '1234567890'
    return render(request, 'sample.html', context={
        'name': name,
        'bmi': bmi,
        'page_url': page_url,
        'fruits': favourite_fruits,
        'msg': msg,
        'msg2': msg2
    })


class Country:

    def __init__(self, name, population, capital):
        self.name = name
        self.population = population
        self.capital = capital

def sample3(request):
    country = Country('Japan', 100000000, 'Tokyo')
    return render(request, 'sample3.html', context={
        'country': country
    })