from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignUpFormTest(TestCase):
    def test_valid_signup_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        form_data = {
            'username': 'testuser',
            'password1': '123',
            'password2': '123'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        form_data2 = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword2'
        }

        form = UserCreationForm(data=form_data2)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


"""
class LoginFormTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.register_url = reverse('signup')

    def test_valid_login_form(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEquals(response.status_code, 200)

        auth_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        auth_form = AuthenticationForm(data=auth_data)
        self.assertTrue(auth_form.is_valid())
"""
