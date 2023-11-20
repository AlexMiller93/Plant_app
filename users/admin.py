from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Profile

# Register your models here.
# admin.site.register(UserFollowing)


class ProfileInline(admin.StackedInline):
    model = Profile


# Unregister Groups
admin.site.unregister(Group)


# Customize User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Register User once more
admin.site.register(User, UserAdmin)
