from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
import datetime #<- 追記
from django.utils import timezone #<- 追記
from .models import Post, Comment
from .services.LoggerService import LoggerService as ls
from .services.AccessService import AccessService
from accounts.models import User
from django.http import Http404

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-published_date').all().exclude(draft_flg='1')
    return render(request, 'bulletin/index.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.publish()
            accessService = AccessService()
            accessService.countup(post)
            return redirect('/post/' + str(post.pk), pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'bulletin/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 記事の作者がログインユーザと違う場合はエラー
    if post.author != request.user:
        raise Http404

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.publish()
            return redirect('/post/' + str(pk), pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'bulletin/post_edit.html', {'form': form})

def post_detail(request, pk):
    # 記事の検索をしつつ、無い場合は404エラーを返す
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(postid=post)
    accessService = AccessService()
    accessService.countup(post)
    return render(request, 'bulletin/post_detail.html', {'post': post,'comments' : comments})

@login_required
def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.postid = post
            comment.published_date = timezone.now()
            comment.publish()
            return redirect('/post/' + str(pk), pk=pk)
    else:
        form = CommentForm()
    return render(request, 'bulletin/comment_edit.html', {'form': form})

@login_required
def comment_edit(request, pk, commentid):
    comment = get_object_or_404(Comment, pk=commentid)
    post = get_object_or_404(Post, pk=pk)
    # コメントの作者が違う場合はエラー
    if comment.author != request.user:
        raise Http404

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.postid = post
            comment.published_date = timezone.now()
            comment.publish()
            return redirect('/post/' + str(pk), pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'bulletin/comment_edit.html', {'form': form })

@login_required
def mypage(request):
    user = get_object_or_404(User, pk=request.user.id)
    return render(request, 'bulletin/mypage.html')

@login_required
def article_list(request):
    user = get_object_or_404(User, pk=request.user.id)
    posts = Post.objects.filter(author=user)
    return render(request, 'bulletin/article_list.html', {'posts': posts })

@login_required
def post_delete(request, pk):
    user = get_object_or_404(User, pk=request.user.id)
    post = get_object_or_404(Post, pk=pk)
    # 記事の作者がログインユーザと違う場合はエラー
    if post.author != request.user:
        raise Http404
    post.delete()
    return redirect('/')
