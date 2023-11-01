from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "title", "short_title",
            "latin_title",
            "category", "description",
            "picture", "appear_date",
            "real_images",
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
            # 'url': forms.HiddenInput(),
        }
        
    # def clean_picture(self):
    #     picture = self.cleaned_data['picture']
    #     valid_extensions = ['jpeg', 'jpg']
    #     extension = picture.rsplit('.', 1).lower()
    #     if extension not in valid_extensions:
    #         raise forms.ValidationError("The given file does n\\'t match valid image extensions")
    #     return picture

    # def clean_images(self):
    #     images = self.cleaned_data['real_images']
    #     valid_extensions = ['jpeg', 'jpg']
    #     extension = images.rsplit('.', 1).lower()
    #     if extension not in valid_extensions:
    #         raise forms.ValidationError("The given file does n\\'t match valid image extensions")
    #     return images


class PlantEditForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "title", "short_title",
            "latin_title",
            "category", "description",
            "picture", "appear_date",
            "real_images",
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
            # 'url': forms.HiddenInput(),
        }
