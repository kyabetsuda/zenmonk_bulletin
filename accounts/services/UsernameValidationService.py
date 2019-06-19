from bulletin.services.LoggerService import LoggerService as ls
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from ..models import User

class UsernameValidationService():

    def validateUsername(self, request, username):
        if request.path == '/accounts/profile_edit/':
            if request.user.username == username:
                return True
            else:
                user = User.objects.filter(username=username)
                return 'そのユーザは既に存在しています' if user else True
        elif request.path == '/accounts/signup/':
            user = User.objects.filter(username=username)
            return 'そのユーザは既に存在しています' if user else True
