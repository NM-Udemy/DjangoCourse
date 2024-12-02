from django.shortcuts import render
from django.views.generic.base import (
    View, TemplateView, RedirectView
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
    FormView,
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from . import forms
from .models import Books, Pictures
from datetime import datetime

class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        book_form = forms.BookForm()
        return render(request, 'index.html' ,context={
            'book_form': book_form,
        })

    def post(self, request, *args, **kwargs):
        book_form = forms.BookForm(request.POST or None)
        if book_form.is_valid():
            book_form.save()
        return render(request, 'index.html', context={
            'book_form': book_form,
        })


class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'message': 'ホームです'
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = kwargs.get('name')
        context['time'] = datetime.now()
        return context

class BookDetailView(DetailView):
    model = Books
    template_name = 'book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'
    slug_field = 'name'
    queryset = Books.objects.filter(price__gt=100)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context.get('book')
        # print(book)
        if book:
            context.update({
                'price_with_tax': book.price * 1.1
            })
        return context


class BookListView(ListView):
    # model = Books
    queryset = Books.objects.all()
    template_name = 'book_list.html'
    ordering = ['price', '-name']
    context_object_name = 'books'
    paginate_by = 3
    
    def get_queryset(self):
        qs = super().get_queryset()
        price_gt = self.request.GET.get('price_gt')
        if price_gt:
            qs = qs.filter(price__gt=price_gt)
        return qs


class BookCreateView(CreateView):
    # model = Books
    # fields = ['name', 'description', 'price']
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('store:list_books')
    # initial = {
    #     'name': 'Name1'
    # }
    
    def form_valid(self, form):
        # form.instance.name = form.instance.name.lower()
        return super().form_valid(form)

class BookUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'update_book.html'
    model = Books
    # fields = ['name', 'description']
    form_class = forms.BookForm
    success_message = '%(name)sに更新しました。値段は%(price)s円です。'
    
    def get_success_url(self):
        return reverse_lazy(
            'store:detail_book', kwargs={'book_id': self.object.pk} # type: ignore
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picture_form = forms.PictureUploadForm()
        context.update(
            {'picture_form': picture_form}
        )
        return context
    
    def form_valid(self, form):
        result = super().form_valid(form)
        picture_form = forms.PictureUploadForm(
            self.request.POST or None, self.request.FILES or None
        )
        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.book = self.object
            picture.save()
        return result

class BookDeleteView(DeleteView):
    model = Books
    template_name = 'delete_book.html'
    success_url = reverse_lazy('store:list_books')


class BookFormView(FormView):
    template_name = 'form_book.html'
    form_class = forms.BookForm
    success_url = reverse_lazy('store:list_books')
    initial = {
        'name': 'Sample'
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BookRedirectView(RedirectView):
    url = reverse_lazy('store:list_books')
    
    def get_redirect_url(self, *args, **kwargs):
        if 'pk' in kwargs:
            book = Books.objects.filter(pk=kwargs['pk']).first()
            if book:
                return reverse_lazy('store:edit_book', kwargs=kwargs)
        return reverse_lazy('store:list_books')


class PictureDeleteView(DeleteView):
    model = Pictures
    
    def get_success_url(self):
        # http referer
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return referer
        
        return reverse_lazy(
            'store:list_books'
        )
