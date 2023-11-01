from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from PIL import Image
from plants.utils import check_path_or_create_dir


def avatar_directory_path(instance, filename):
    path = f"images/users/{instance.user.username}/avatar/"
    return check_path_or_create_dir(path, filename)


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        default='images/default.png',
        upload_to=avatar_directory_path,
        null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    age = models.PositiveSmallIntegerField(null=True)
    rating = models.DecimalField(
        default=1.0, max_digits=4,
        decimal_places=2, blank=True, null=True)

    class UserStatus(models.TextChoices):
        BEGINNER = 'Beginner'
        AMATEUR = 'Amateur'
        EXPERT = 'Expert'
        MASTER = 'Master'

    user_status = models.CharField(
        max_length=8, choices=UserStatus.choices,
        default=UserStatus.BEGINNER
    )

    class Sex(models.TextChoices):
        WOMEN = 'W'
        MEN = 'M'

    sex = models.CharField(
        max_length=10, choices=Sex.choices, default=Sex.MEN)

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

        if self.birth_date:
            import datetime
            today = datetime.date.today()
            self.age = today.year - self.birth_date.year
            if today.month < self.birth_date.month or today.month == self.birth_date.month and today.day < self.birth_date.day:
                self.age -= 1
        return super().save(*args, **kwargs)
