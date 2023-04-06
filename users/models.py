from django.contrib.auth.models import User
from django.db import models
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        default='images/default.jpg',
        upload_to='images/users/{{ user.username }}/avatar/',
        null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "profile"
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_profile', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        import random
        if not self.slug:
            self.slug = random.randint(1, 1000)
        return super().save(*args, **kwargs)
        
        '''
        img = Image.open(self.avatar.url) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.avatar.url) # Save it again and override the larger image
        '''
    
    
    '''
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
    '''
    
    
    
    
    
    
    
    