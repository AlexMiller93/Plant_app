from django.urls import path

from .views import (
    HomeView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    
    # CRUD function
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post/edit/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
]