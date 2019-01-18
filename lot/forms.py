from django import forms
from .models import Question


class NewQuestionForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Question
        fields = ['subject', 'message']
