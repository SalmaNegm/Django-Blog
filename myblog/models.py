from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Post(models.Model):
    title=models.CharField(max_length=255,)
    content=models.TextField(max_length=1000)
    image=models.ImageField(upload_to='posts/%Y/%m')
    pub_date=models.DateTimeField(null=True)
    num_views=models.PositiveSmallIntegerField(default=0)
    is_published=models.BooleanField()

    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content=models.TextField(max_length=200)
    creation_date=models.DateTimeField(auto_now_add=True)
    modification_date=models.DateTimeField(auto_now=True)

    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    likes=models.ManyToManyField(User,related_name='liked_by')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='writer')
    post=models.ForeignKey('Post',on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Tag(models.Model):
    name=models.CharField(max_length=255)
    post=models.ManyToManyField('Post')

