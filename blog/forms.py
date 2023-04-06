from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'title_tag', 'author', 'slug', 'content')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}), 
            # 'author': forms.Select(attrs={'class': 'form-control'}), 
            'content': forms.Textarea(attrs={'class': 'form-control'}), 
        }
        
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'title_tag', 'content')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}), 
            'content': forms.Textarea(attrs={'class': 'form-control'}), 
        }