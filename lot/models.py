from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.text import slugify
from markdown import markdown
import pytz

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]


class Lot(models.Model):
    """
    Represents a group of people (typically at a training) that
    will want to post questions.
    """
    group_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    slug = models.SlugField(unique=True)
    timezone = models.CharField(max_length=100, choices=TIMEZONE_CHOICES,
                                default='America/Los_Angeles')

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
    """
    Represents an individual question within a training.
    Note the first message/post actually contains the question,
    although it is summarized in the subject
    """
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot, related_name='questions',
                            on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='questions',
                                on_delete=models.CASCADE)
    starter_name = models.CharField(max_length=100, default='Anonymous')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_first_post(self):
        return (Post.objects.filter(question=self)
                .order_by('created_at')
                .first())


class Post(models.Model):
    """
    Synonymous with comment.
    """
    message = models.TextField(max_length=4000)
    question = models.ForeignKey(Question, related_name='posts',
                                 on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, null=True, related_name='posts',
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',
                                   on_delete=models.CASCADE)

    created_name = models.CharField(max_length=100)
    updated_name = models.CharField(max_length=100)

    def __str__(self):
        return self.message[:30]

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
