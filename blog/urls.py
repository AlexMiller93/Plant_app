from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(),
         name='post_detail'),

    # CRUD classes for posts
    path('post_create/', views.PostCreateView.as_view(),
         name='post_create'),
    path('post/edit/<slug:slug>/', views.PostUpdateView.as_view(),
         name='post_edit'),
    path('post/delete/<slug:slug>/', views.PostDeleteView.as_view(),
         name='post_delete'),

    # post list classes
    path('user_posts/<int:pk>/', views.UserPostListView.as_view(),
         name='user_posts'),
    path('tag_posts/<str:tag>/', views.TagPostListView.as_view(),
         name='tag_posts'),
    path('search_posts/', views.SearchPostListView.as_view(),
         name='search_posts'),
    path('status_posts/<str:status>/', views.OneStatusPostListView.as_view(),
         name='status_posts'),
    path('favorites_posts/<int:pk>', views.FavoritesPostListView.as_view(),
         name='favorites_posts'),

    path('most_liked/', views.MostLikedPostListView.as_view(),
         name='most_liked_posts'),
    path('most_commented/', views.MostCommentedPostListView.as_view(),
         name='most_commented_posts'),
    path('most_visited/', views.MostViewPostListView.as_view(),
         name='most_visited_posts'),
    path('reverse_order/', views.ChangeOrderPostListView.as_view(),
         name='change_order'),

    # post comment classes
    path('post/<slug:slug>/comment/<int:pk>/edit_comment/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('post/<slug:slug>/comment/<int:pk>/delete_comment/',
         views.CommentDeleteView.as_view(), name='delete_comment'),

    # post functions
    path('post_like/<slug:slug>/', views.post_like, name='post_like'),
    path('comment_like/<slug:slug>/comment/<int:pk>', views.comment_like,
         name='comment_like'),
    path('post_favorites/<slug:slug>', views.add_favorites,
         name='add_post_favorites'),
    path('post_shared/<slug:slug>', views.share_post, name='share_post'),
]
