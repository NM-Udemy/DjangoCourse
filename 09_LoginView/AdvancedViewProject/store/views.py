from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Items
from django.http import Http404
# Create your views here.

def item_list(request):
    items = Items.objects.all()
    # items = get_list_or_404(Items, pk__gt=4)
    return render(request, 'store/item_list.html', context={
        'items': items
    })


def item_detail(request, id):
    if id == 0:
        raise Http404
    # item = Items.objects.filter(pk=id).first()
    # item = get_object_or_404(Items, name='りんご', pk=id)
    item = get_object_or_404(Items, pk=id)
    if item is None:
        return redirect('store:item_list')
    return render(request, 'store/item_detail.html', context={
        'item': item
    })

def to_google(request):
    return redirect('https://www.google.com')

def one_item(request):
    return redirect('store:item_detail', id=1)

def page_not_found(request, exception):
    return render(request, 'store/404.html', status=404)
    # return redirect('store:item_list')

def server_error(request):
    return render(request, 'store/500.html', status=500)
