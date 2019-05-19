from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserManager
from bulletin.services.LoggerService import LoggerService as ls

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'] )
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form':form})

def profile_edit(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            ls.file(user.password)
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('/')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/profile_edit.html', {'form':form})
