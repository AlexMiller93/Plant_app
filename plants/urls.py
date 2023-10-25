from django.urls import path

from . import views

urlpatterns = [
    path('user_feed/<int:pk>/', views.UserFeedPlantsView.as_view(),
         name="feed_plants"),
    path('user_plants/<int:pk>/', views.UserPlantsView.as_view(),
         name="user_plants"),
    path('plant/<slug:slug>/', views.PlantDetailView.as_view(),
         name="plant_detail"),

    # CRUD for plants
    path('add/', views.PlantCreateView.as_view(),
         name='plant_add'),
    path('edit/<slug:slug>/', views.PlantUpdateView.as_view(),
         name='plant_edit'),
    path('delete/<slug:slug>/', views.PlantDeleteView.as_view(),
         name='plant_delete'),

    # other plant classes
    path('category_plants/<str:category>', views.CategoryPlantView.as_view(),
         name='category_plants'),
    path('latin_plants/<str:latin_title>', views.LatinNamePlantView.as_view(),
         name='latin_plants'),
    path('favorites_plants/<int:pk>', views.FavoritesPlantView.as_view(),
         name='favorites_plants'),
    path('most_liked/', views.MostLikedPlantView.as_view(),
         name='most_liked_plants'),
    path('most_viewed/', views.MostViewedPlantView.as_view(),
         name='most_viewed_plants'),

    # some functions
    path('plant_like/<slug:slug>/', views.plant_like, name='plant_like'),
    path('plant_favorites/<slug:slug>', views.add_favorites, name='add_plant_favorites'),
]
