from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import CommentForm, EmailPostForm
from .models import Post

app_name = 'news'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # tag = None

    # if tag_slug:
    #   tag = get_object_or_404(Tag, slug=tag_slug)
    #  object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 post in each page.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if it aint no integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if the page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'news/news_article_list.html', {'page': page, 'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    # list of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # a user is trying to post a comment
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post a comment")
            return redirect(reverse('login') + '?next=' + request.path)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save it
            new_comment = comment_form.save(commit=False)
            # assign current post to the comment
            new_comment.post = post
            # comments are active immediately (moderation can flip this later)
            new_comment.active = True
            # save the comment to the db
            new_comment.save()
            messages.success(request, "Your comment has been added")
            return redirect(reverse('news:post_detail', args=[post.slug]) + '#comments')
        else:
            messages.error(request, "Your comment could not be added, please check the form")
    else:
        # prefill the name for logged in users
        if getattr(request, 'user', None) is not None and request.user.is_authenticated:
            comment_form = CommentForm(initial={'name': request.user.username})
        else:
            comment_form = CommentForm()

    return render(request, 'news/news_article_detail.html', {'post': post, 'comments': comments,
                                                             'comment_form': comment_form,
                                                             'new_comment': None})


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form was submited
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # subject of the email.
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'noreply@nfmstudios.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'news/news_share_post.html', {'post': post, 'form': form, 'sent': sent})