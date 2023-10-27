from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'tags', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': TagWidget(),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'tags', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': TagWidget(),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'reply')

        labels = {
            'content': _(''),
        }

        widgets = {
            'content': forms.TextInput(attrs={})
        }


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

        labels = {
            'content': _(''),
        }

        widgets = {
            'content': forms.TextInput(attrs={})
        }
