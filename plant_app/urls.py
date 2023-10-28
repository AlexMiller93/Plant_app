"""plant_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSitemap, CommentSitemap

from users import views

sitemaps = {
    'posts': PostSitemap,
    # 'comments': CommentSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    path('', include('blog.urls')),
    path('plants/', include('plants.urls')),
    path('users/', include('users.urls')),
    path('users/', include("django.contrib.auth.urls")),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(),
         name='user_profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(),
         name='update_profile'),

    # sitemap staff
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
