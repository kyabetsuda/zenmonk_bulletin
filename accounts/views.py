from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserManager
from bulletin.services.LoggerService import LoggerService as ls
from .services.RandomStringService import RandomStringService as rss
from .services.UsernameValidationService import UsernameValidationService as uvs
from django.db.models.fields.files import FieldFile

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            uv = uvs()
            message = uv.validateUsername(request, username)
            if not type(message) is bool: return render(request, 'accounts/signup.html', {'form':form, 'message':message})
            User.objects.create_user(username, form.cleaned_data['email'], form.cleaned_data['password'] )
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form':form})

def profile_edit(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        #画像のアップロード(request.FILES)
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            uv = uvs()
            # ユーザネーム検証
            message = uv.validateUsername(request, user.username)
            if not type(message) is bool: return render(request, 'accounts/profile_edit.html', {'form':form, 'message':message})
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            # 画像更新時の処理
            # 元の画像を保持
            tmp_img = user.profile_img
            # フォームの値をセット
            user.profile_img = form.cleaned_data['profile_img']
            # 画像の型がFieldFileである、かつ名前がNoneじゃない(=画像がセットされている)
            if type(user.profile_img) is FieldFile and user.profile_img.name != None:
                user.profile_img.name = rss.generateRandomString(8) + ".jpg"
            # 画像の型がFieldFileである、かつ名前がNoneである(=画像がセットされていない)
            elif not type(user.profile_img) is bool:
                # 元の画像そのまま突っ込む
                user.profile_img = tmp_img
            user.save()
            return redirect('/')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/profile_edit.html', {'form':form})
