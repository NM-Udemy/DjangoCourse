from django.shortcuts import render, redirect

def page_not_found(request, exception):
    print(exception)
    return render(request, '404.html', status=404)
    # return redirect('store:item_list')
    
def server_error(request):
    return render(request, '500.html', status=500)
