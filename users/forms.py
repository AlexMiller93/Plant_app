from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.forms.widgets import DateInput, EmailInput, TextInput, FileInput

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'bio',
            'location',
            'birth_date',
            'user_status',
            'sex'
        ]

        labels = {
            'birth_date': 'Your birthday'
        }

        widgets = {
            'avatar': FileInput(attrs={'type': 'file'}),
            'bio': TextInput(attrs={'type': 'text'}),
            'location': TextInput(attrs={'type': 'text'}),
            'birth_date': DateInput(attrs={'type': 'date'})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

        widgets = {
            'username': TextInput(attrs={'type': 'text'}),
            'first_name': TextInput(attrs={'type': 'text'}),
            'last_name': TextInput(attrs={'type': 'text'}),
            'email': EmailInput(attrs={'type': 'email'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #  dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
