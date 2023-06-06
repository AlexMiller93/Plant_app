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
    MostLikedPostListView,
    MostCommentedPostListView,
    ChangeOrderPostListView,
    CommentUpdateView,
    CommentDeleteView,
    FavoritesPostListView,
    PostLike,
    AddFavorites,
    CommentLike,
    SharePost
    )


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), 
        name='post_detail'),
    
    # CRUD classes for posts
    path('post_create/', PostCreateView.as_view(), 
        name='post_create'),
    path('post/edit/<slug:slug>/', PostUpdateView.as_view(), 
        name='post_edit'),
    path('post/delete/<slug:slug>/', PostDeleteView.as_view(), 
        name='post_delete'),
    
    # post list classes
    path('user_posts/<int:pk>/', UserPostListView.as_view(), 
        name='user_posts'),
    path('tag_posts/<str:tag>/', TagPostListView.as_view(),
        name='tag_posts'),
    path('search_posts/', SearchPostListView.as_view(), 
        name='search_posts'),
    path('status_posts/<str:status>/', OneStatusPostListView.as_view(),
        name='status_posts'),
    path('favorites_posts/<int:pk>', FavoritesPostListView.as_view(), 
        name='favorites_posts'),
    
    path('most_liked/', MostLikedPostListView.as_view(), 
        name='most_liked_posts'),
    path('most_commented/', MostCommentedPostListView.as_view(), 
        name='most_commented_posts'),
    path('reverse_order/', ChangeOrderPostListView.as_view(), 
        name='change_order'),
    
    # post comment classes
    path('post/<slug:slug>/comment/<int:pk>/edit_comment/',
        CommentUpdateView.as_view(), name='edit_comment'),
    path('post/<slug:slug>/comment/<int:pk>/delete_comment/',
        CommentDeleteView.as_view(), name='delete_comment'),
    
    # post functions
    path('post_like/<slug:slug>/', PostLike, name='post_like'),
    path('comment_like/<slug:slug>/comment/<int:pk>', CommentLike, 
        name='comment_like'),
    path('post_favorites/<slug:slug>', AddFavorites, 
        name='add_post_favorites'),
    path('post_shared/<slug:slug>', SharePost, name='share_post'),
]