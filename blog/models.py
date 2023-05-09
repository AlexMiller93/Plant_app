from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.models import Profile

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=128)
    tag = models.CharField(max_length=128)
    author = models.ForeignKey(Profile, 
            related_name='posts',
            on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    content = models.TextField(
        help_text="You can write your thoughts here...", 
        blank=True, null=True)
    images = models.ImageField(
        upload_to='images/users/plants/',
        help_text="Upload images with your plants",
        height_field=100, width_field=200,
        null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    post_noted = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        Profile, related_name="post_like", blank=True)
    seen_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL
        )
    
    class Meta:
        verbose_name = "post"
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    def get_comments(self):
        return self.comments.filter(reply=None)
    
    def get_replies(self):
        return self.comments.exclude(reply=None)
    
    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def generate_slug(self, save_to_obj=False, add_random_suffix=True):
        """
        Generates and returns slug for this obj.
        If `save_to_obj` is True, then saves to current obj.
        Warning: setting `save_to_obj` to True
            when called from `.save()` method
            can lead to recursion error!

        `add_random_suffix ` is to make sure that slug field has unique value.
        """

        # We rely on django's slugify function here. But if
        # it is not sufficient for you needs, you can implement
        # you own way of generating slugs.
        generated_slug = slugify(self.title)

        # Generate random suffix here.
        import random, string
        random_suffix = ""
        if add_random_suffix:
            random_suffix = ''.join([
                random.choice(string.digits)
                for i in range(3)
            ])
            generated_slug += '-%s' % random_suffix

        if save_to_obj:
            self.slug = generated_slug
            self.save(update_fields=['slug'])
        
        return generated_slug
    
class Share(Post):
    post = models.ForeignKey(Post, related_name="shared_post", on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(
        help_text="Write comment",
        blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Profile, related_name="comment_like", blank=True)
    reply = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        verbose_name = "comment"
        ordering=['-created_on']
    
    def __str__(self):
        return self.content 
    
    @property
    def children(self):
        return Comment.objects.filter(reply=self).reverse()

    @property
    def is_parent(self):
        if self.reply is None:
            return True
        return False
    
