from django.contrib.sitemaps import Sitemap
from .models import Post, Comment


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_on


class CommentSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Comment.objects.all()

    def lastmod(self, obj):
        return obj.updated_on
