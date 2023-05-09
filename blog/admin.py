from django.contrib import admin

from .models import Post, Comment

# Register your models here.

admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'slug', 'author')
    list_filter = ('created_on', 'author', 'tag')
    search_fields = ('title', 'author', 'content')


admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'post', 'created_on')
    list_filter = ('created_on', 'updated_on')
    search_fields = ('author', 'content')
