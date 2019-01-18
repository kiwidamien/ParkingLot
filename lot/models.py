from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Lot(models.Model):
    group_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super(Lot, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    def get_comments_count(self):
        return Post.objects.filter(question__lot=self).count()

    def get_last_comment(self):
        return (Post.objects.filter(question__lot=self)
                .order_by('-created_at')
                .first())


class Question(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot, related_name='questions',
                            on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='questions',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


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

    def __str__(self):
        return self.message[:30]
