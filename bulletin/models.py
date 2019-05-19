from django.db import models
from django.utils import timezone
from accounts.models import User


class Post(models.Model):
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    draft_flg = models.CharField(max_length=1, default='0')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    postid = models.ForeignKey('bulletin.Post', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Access(models.Model):
    postid = models.ForeignKey('bulletin.Post', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
