from django import forms
from .models import User
from bulletin.services.LoggerService import LoggerService as ls
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

class UserForm(forms.ModelForm):

    password = forms.CharField(
        label='パスワード',
        max_length=150,
        required=True,
        help_text='8文字以上で入力してください',
        widget=forms.PasswordInput(), min_length=8
    )

    cpassword = forms.CharField(
        label='パスワード確認用',
        max_length=150,
        required=True,
        help_text='8文字以上で入力してください',
        widget=forms.PasswordInput(), min_length=8
    )

    # profile_img = forms.ImageField()

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        cpassword = self.cleaned_data.get('cpassword', None)
        if not password or not cpassword or (password != cpassword):
            raise forms.ValidationError('パスワードが確認用と一致しません')
        return password


    class Meta:
        model = User
        fields = (
        'username',
        'cpassword',
        'password',
        'email',
        'profile_img'
        )
