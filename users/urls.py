from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(),
         name='user_profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(),
         name='update_profile'),
]
