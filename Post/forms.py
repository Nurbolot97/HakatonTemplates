from django import forms
from . models import *
from django.forms import Textarea, ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'col': 50, 'rows': 2}),
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'photo', 'slug', 'tags')

















