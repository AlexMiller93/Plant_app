from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from .. models import Profile

class TestViews(TestCase):
    ''' Testing signup-login-logout functions for User objects'''

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('signup')

    def test_signup_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'testuser@gmail.com',
            
            'password': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEquals(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEquals(response.status_code, 200)

class ProfileViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="user1", 
            email="user1@gmail.com",
            password="qwerty",
            # bio="I'm first test profile",
            # avatar=None,
            # location="New York",
            # birth_date="1990-01-01",
        )
        
        cls.user2 = User.objects.create_user(
            username="user2", 
            email="user2@gmail.com",
            password="qwerty",
            # bio="I'm second test profile",
            # avatar=None,
            # location="Paris",
            # birth_date="1995-12-31",
        )
    
    def test_returns_200(self):
        self.client.login(email="user1@gmail.com", password="qwerty")
        response = self.client.get(reverse(
            "user_profile", kwargs=({"pk": self.user1.pk}))
        )

        self.assertEqual(response.status_code, 200)
    
'''
class SignupPageTests(TestCase):
    # https://github.com/wsvincent/djangoforbeginners/blob/master/ch15-comments/accounts/tests.py
    
    def test_url_exists_at_correct_location_signup_view(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@gmail.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")
        self.assertEqual(get_user_model().objects.all()[0].email, "testuser@gmail.com")
    '''