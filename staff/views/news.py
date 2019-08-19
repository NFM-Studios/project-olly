from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from staff.forms import *
from wagers.models import *


def news_list(request):
    # get all teh news articles
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        news_list = Post.objects.all().order_by('-id')
        return render(request, 'staff/news/news_list.html', {'news_list': news_list})


def create_article(request):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'POST':
            form = ArticleCreateForm(request.POST, request.FILES)
            if form.is_valid():
                article = form.instance
                article.author = User.objects.get(username=request.user.username)
                article.save()
                form.save()
                messages.success(request, 'Your post has been created')
                return redirect('staff:news_list')
            else:
                return render(request, 'staff/news/create_article.html', {'form': form})
        else:
            form = ArticleCreateForm(None)
            return render(request, 'staff/news/create_article.html', {'form': form})


def detail_article(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        article = Post.objects.get(id=pk)
        return render(request, 'staff/news/news_detail.html', {'article': article})


def edit_post(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        if request.method == 'GET':
            article = get_object_or_404(Post, pk=pk)
            form = EditNewsPostForm(instance=article)
            return render(request, 'staff/news/edit_article.html', {'form': form})
        else:
            article = get_object_or_404(Post, pk=pk)
            form = EditNewsPostForm(request.POST, instance=article)
            if form.is_valid():
                post = form.instance
                post.author = request.user
                post.save()
                messages.success(request, "Updated post")
                return redirect('staff:detail_article', pk=pk)
            else:
                return render(request, 'staff/news/edit_article.html', {'form': form})


def delete_article(request, pk):
    user = UserProfile.objects.get(user__username=request.user.username)
    allowed = ['superadmin', 'admin']
    if user.user_type not in allowed:
        return render(request, 'staff/permissiondenied.html')
    else:
        article = Post.objects.get(pk=pk)
        article.delete()
        messages.success(request, 'Post has been deleted')
        return redirect('staff:news_index')
