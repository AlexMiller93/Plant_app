
import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag()
def show_latest_posts(pk=None, count=2):
    if pk:
        latest_posts = Post.objects.filter(author__id=pk).order_by('-created_on')[:count]
    else:
        latest_posts = Post.objects.all().order_by('-created_on')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag()
def get_most_liked_posts(pk=None, count=2):
    if pk:
        return Post.objects.filter(author__id=pk).annotate(
            total_likes=Count('likes')).order_by('-created_on')[:count]
    else:
        return Post.objects.annotate(
            total_likes=Count('likes')).order_by('-created_on')[:count]


@register.simple_tag()
def get_most_commented_posts(pk=None, count=2):
    if pk:
        return Post.objects.filter(author__id=pk).annotate(
            total_likes=Count('comments')).order_by('-created_on')[:count]
    else:
        return Post.objects.annotate(
            total_likes=Count('comments')).order_by('-created_on')[:count]


@register.simple_tag()
def get_most_visited_posts(pk=None, count=5):
    if pk:
        return Post.objects.filter(author__id=pk).annotate(
            total_likes=Count('seen_by')).order_by('-created_on')[:count]
    else:
        return Post.objects.annotate(
            total_likes=Count('seen_by')).order_by('-created_on')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

