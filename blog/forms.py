from django import forms

from .models import Post

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
        