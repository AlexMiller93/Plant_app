from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, blank=True, null=True)
    
    first_name = models.CharField(max_length=70, blank=True, null=True)
    last_name = models.CharField(max_length=70, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    email = models.EmailField(max_length=254)
    
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', )
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    
    class Meta:
        db_table = "profile"
    
    
    @property
    def edit_username(self):
        " Returns user's username."
        # if user didn't input username
        if not self.username:
            self.username = '@' + self.user.lower()
        self.username = '@' + self.username
        
        return self.username
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property 
    def add_slug(self):
        import random
        if not self.slug:
            self.slug = random.randint()
    
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_profile', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.username
    
    