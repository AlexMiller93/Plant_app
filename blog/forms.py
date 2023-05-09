from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'tag', 'content')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'tag': forms.TextInput(attrs={'class': 'form-control'}), 
            'content': forms.Textarea(attrs={'class': 'form-control'}), 
        }
        
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'tag', 'content')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'tag': forms.TextInput(attrs={'class': 'form-control'}), 
            'content': forms.Textarea(attrs={'class': 'form-control'}), 
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
    
        
        # labels = {
        #     'content': _(''),
        # }
        
        widgets = {
            'content': forms.TextInput(attrs={})
        }

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
        # labels = {
        #     'content': _(''),
        # }
        
        widgets = {
            'content': forms.TextInput(attrs={})
        }