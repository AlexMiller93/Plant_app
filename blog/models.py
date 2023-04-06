from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from PIL import Image

from users.models import Profile

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    title_tag = models.CharField(max_length=128)
    author = models.ForeignKey(Profile, 
            on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    content = models.TextField(
        help_text="You can write your thoughts here...", 
        blank=True, null=True)
    
    images = models.ImageField(
        upload_to='images/users/{{ user.username }}/plants/',
        help_text="Upload images with your plants",
        height_field=100, width_field=200,
        null=True, blank=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    post_noted = models.BooleanField(default=False)
    # likes = models.ManyToManyField("self")
    
    class Meta:
        verbose_name = "post"
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(
        help_text="Write comment",
        blank=True, null=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("self")
    
    
    class Meta:
        verbose_name = "comment"
    
    def __str__(self):
        return self.text 
    
    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})