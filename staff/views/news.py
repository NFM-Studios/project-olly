from staff.auth import staff_required
from django.http import HttpResponseNotAllowed

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from staff.forms import *
from wagers.models import *


@staff_required
def news_list(request):
    # get all teh news articles
    news_list = Post.objects.all().order_by('-id')
    return render(request, 'staff/news/news_article_list.html', {'news_list': news_list})


@staff_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.instance
            article.author = User.objects.get(username=request.user.username)
            article.save()
            form.save()
            messages.success(request, 'Your post has been created')
            return redirect('staff:news_index')
        else:
            return render(request, 'staff/news/news_article_create.html', {'form': form})
    else:
        form = ArticleCreateForm(None)
        return render(request, 'staff/news/news_article_create.html', {'form': form})


@staff_required
def detail_article(request, pk):
    article = Post.objects.get(id=pk)
    return render(request, 'staff/news/news_article_detail.html', {'article': article})


@staff_required
def edit_post(request, pk):
    if request.method == 'GET':
        article = get_object_or_404(Post, pk=pk)
        form = EditNewsPostForm(instance=article)
        return render(request, 'staff/news/news_article_edit.html', {'form': form})
    else:
        article = get_object_or_404(Post, pk=pk)
        form = EditNewsPostForm(request.POST, instance=article)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = article.author
            post.save()
            messages.success(request, "Updated post")
            return redirect('staff:detail_article', pk=pk)
        else:
            return render(request, 'staff/news/news_article_edit.html', {'form': form})


@staff_required
def delete_article(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    article = Post.objects.get(pk=pk)
    article.delete()
    messages.success(request, 'Post has been deleted')
    return redirect('staff:news_index')
