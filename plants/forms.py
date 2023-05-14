from django import forms
from  .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "title", "short_title", 
            "latin_title",
            "category", "description", 
            "picture", "appear_date", 
            "real_images"
            ]
            
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'short_title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'latin_title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'category': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text'}), 
            'picture': forms.FileInput(attrs={'type': 'file'}),
            'appear_date': forms.DateInput(attrs={'type': 'date'}),
            'real_images': forms.FileInput(attrs={'type': 'file'}),
        }
        
class PlantEditForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "title", "short_title", 
            "latin_title",
            "category", "description", 
            "picture", "appear_date", 
            "real_images"
            ]
            
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'short_title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'latin_title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'category': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}), 
            'description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text'}), 
            'picture': forms.FileInput(attrs={'type': 'file'}),
            'appear_date': forms.DateInput(attrs={'type': 'date'}),
            'real_images': forms.FileInput(attrs={'type': 'file'}),
        }
