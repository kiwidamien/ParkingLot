from django import forms
from django.utils.text import slugify
from .models import Question, Post, Lot


class NewQuestionForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Question
        fields = ['subject', 'message', ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class CreateLotForm(forms.ModelForm):
    class Meta:
        model = Lot 
        fields = '__all__'

class FindLotForm(forms.Form):
    lot_slug = forms.CharField(max_length=100,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'col-8 rounded',
                                       'placeholder': 'Parking lot name'
                                   }
                               )
                              )

    def clean(self):
        cleaned_data = super(FindLotForm, self).clean()
        the_slug = cleaned_data.get('lot_slug')
        if not the_slug:
            raise forms.ValidationError('Please add a Parking Lot name')
        the_slug = slugify(the_slug)
        try:
            Lot.objects.get(slug=the_slug)
        except Lot.DoesNotExist:
            raise forms.ValidationError('That Parking Lot does not exist')


