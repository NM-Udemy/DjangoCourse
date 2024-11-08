from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms
from .models import Theme, Comment
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.core.cache import cache

@login_required
def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid():
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request, '掲示板を作成しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/create_theme.html', context={
            'create_theme_form': create_theme_form,
        }
    )

def list_themes(request):
    themes = Theme.objects.fetch_all_themes()
    return render(
        request, 'boards/list_themes.html', context={
            'themes': themes,
        }
    )

@login_required
def edit_theme(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    if theme.user.pk != request.user.pk:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(
        request.POST or None, instance=theme
    )
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'pk': pk,
        }
    )
    
@login_required
def delete_theme(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    if theme.user.pk != request.user.pk:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():
        theme.delete()
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )
    
@login_required
def post_comment(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    comments = Comment.objects.fetch_by_theme_id(theme_id)
    cached_comment = cache.get(
        f'save_comment_theme_id={theme_id}_user_id={request.user.id}'
    )
    post_comment_form = forms.PostCommentForm(
        request.POST or None, initial={'comment': cached_comment}
    )
    if post_comment_form.is_valid():
        post_comment_form.instance.user = request.user
        post_comment_form.instance.theme = theme
        post_comment_form.save()
        if cached_comment:
            cache.delete(
                f'save_comment_theme_id={theme_id}_user_id={request.user.id}'
            )
        return redirect('boards:post_comment', theme_id=theme_id)
    return render(
        request, 'boards/post_comment.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )

@login_required
def save_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        comment = request.POST.get('comment')
        theme_id = request.POST.get('theme_id')
        if comment and theme_id:
            cache.set(
                f'save_comment_theme_id={theme_id}_user_id={request.user.id}',
                comment
            )
            return JsonResponse({'message': '一時保存しました。'})
    return JsonResponse({'error': '無効なリクエストです。'})