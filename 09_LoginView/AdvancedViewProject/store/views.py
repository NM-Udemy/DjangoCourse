from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Items
from django.http import Http404
# Create your views here.

def item_list(request):
    # items = Items.objects.all()
    items = get_list_or_404(Items, price__gt=50, pk__gt=1)
    return render(
        request, 'store/item_list.html', context={
            'items': items,
        }
    )

def item_detail(request, id):
    # if id == 0:
    #     raise Http404('idが0です')
    # try:
    #     item = Items.objects.get(pk=id)
    # except:
    #     return redirect('store:item_list')
    item = get_object_or_404(Items, pk=id)
    return render(request, 'store/item_detail.html', context={
        'item': item,
    })

def to_google(request):
    return redirect('https://www.google.com')

def one_item(request):
    return redirect('store:item_detail', id=1)
