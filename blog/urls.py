from django.urls import path

from .views import (
    HomeView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    TagPostListView,
    SearchPostListView,
    OneStatusPostListView,
    PostLike,
    PostNote,
    )

from blog.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), 
        name='post_detail'),
    
    # CRUD function for posts
    path('post_create/', PostCreateView.as_view(), 
        name='post_create'),
    path('post/edit/<slug:slug>/', PostUpdateView.as_view(), 
        name='post_update'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(), 
        name='post_delete'),
    
    path('user_posts/<int:pk>/', UserPostListView.as_view(), 
        name='user_posts'),
    path('tag_posts/<str:tag>/', TagPostListView.as_view(),
        name='tag_posts'),
    path('search_posts/', SearchPostListView.as_view(), 
        name='search_posts'),
    path('status_posts/<str:status>/', OneStatusPostListView.as_view(),
        name='status_posts'),
    
    path('like/<slug:slug>/', PostLike, name='post_like'),
    
    path('post_noted/', PostNote, name='change_post_noted'),
]