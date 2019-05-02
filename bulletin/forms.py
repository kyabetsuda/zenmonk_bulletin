from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    CHOICE = {
        ('0','公開'),
        ('1','下書き'),
    }
    draft_flg = forms.ChoiceField(label='状態', widget=forms.RadioSelect, choices= CHOICE, initial=0)

    class Meta:
        model = Post
        fields = ('title', 'text', 'draft_flg',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
