from django import forms
from .models import Question, Post


class NewQuestionForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Question
        fields = ['subject', 'message', ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
