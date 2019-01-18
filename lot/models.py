from django.db import models
from django.contrib.auth.models import User


class Lot(models.Model):
    group_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class Question(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot, related_name='questions',
                            on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='questions',
                                on_delete=models.CASCADE)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    question = models.ForeignKey(Question, related_name='posts',
                                 on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts',
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',
                                   on_delete=models.CASCADE)
