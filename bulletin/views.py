from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
import datetime #<- 追記
from django.utils import timezone #<- 追記
from .models import Post, Comment

# Create your views here.
@login_required
def index(request):
    posts = Post.objects.all()
    return render(request, 'bulletin/index.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'bulletin/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'bulletin/post_edit.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'bulletin/post_detail.html', {'post': post})

@login_required
def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, pk=pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.postid = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('/', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'bulletin/comment_edit.html', {'form': form})

@login_required
def comment_edit(request, pk, commentid):
    comment = get_object_or_404(Comment, pk=commentid)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.postid = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('/post/' + str(pk), pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'bulletin/comment_edit.html', {'form': form})
