from django.db import models
from django.conf import settings
from users.models import Profile
from blog.models import Post


# Create your models here.
class Plant(models.Model):
    title = models.CharField(max_length=128)
    short_title = models.CharField(max_length=128, null=True, blank=True)
    latin_title = models.CharField(max_length=128)
    category = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(
        help_text="You can write some description about your plant ...",
        blank=True, null=True)

    owner = models.ForeignKey(Profile,
                              related_name='plants',
                              on_delete=models.CASCADE)

    picture = models.ImageField(
        default='images/plant_default.png',
        upload_to='images/users/plants/picture/',
        null=True, blank=True)

    appear_date = models.DateField(null=True, blank=True)
    duration = models.PositiveSmallIntegerField(null=True)
    slug = models.SlugField(unique=True)

    real_images = models.ImageField(
        upload_to='images/users/plants/images/',
        help_text="Upload images with your plants",
        height_field=100, width_field=200,
        null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    fav_plants = models.ManyToManyField(
        Profile, related_name="favorites_plants", blank=True)
    likes = models.ManyToManyField(
        Profile, related_name="plant_like", blank=True)

    rel_posts = models.ManyToManyField(
        Post, related_name="plant_posts", blank=True)
    seen_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="plant_view"
    )

    class Meta:
        verbose_name = "plant"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plant_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            import random
            self.slug = random.randint(1, 10000)

        if self.appear_date:
            import datetime
            today = datetime.date.today()
            self.duration = today.year - self.appear_date.year
            if today.month < self.appear_date.month or today.month == self.appear_date.month and today.day < self.appear_date.day:
                self.duration -= 1
        return super().save(*args, **kwargs)
