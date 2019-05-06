from ..models import Post, Access
from .LoggerService import LoggerService as ls

class AccessService():


    def countup(self, post):
        try:
            access = Access.objects.get(postid=post)
            access.count = access.count + 1
            access.publish()
        except:
            access = Access(postid=post)
            access.publish()
