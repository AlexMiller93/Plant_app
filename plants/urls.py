from django.urls import path

from .views import (
    UserFeedPlantsView,
    UserPlantsView,
    PlantDetailView,
    PlantCreateView,
    PlantUpdateView,
    PlantDeleteView,
    CategoryPlantView,
    LatinNamePlantView,
    FavoritesPlantView,
    MostLikedPlantView,
    MostViewedPlantView,
    PlantLike,
    AddFavorites,
)

urlpatterns = [
    path('user_feed/<int:pk>/', UserFeedPlantsView.as_view(), 
        name="feed_plants"),
    path('user_plants/<int:pk>/', UserPlantsView.as_view(), 
        name="user_plants"),
    path('plant/<slug:slug>/', PlantDetailView.as_view(),
        name="plant_detail"),
    
    # CRUD for plants
    path('add/', PlantCreateView.as_view(), 
        name='plant_add'),
    path('edit/<slug:slug>/', PlantUpdateView.as_view(), 
        name='plant_edit'),
    path('delete/<slug:slug>/', PlantDeleteView.as_view(), 
        name='plant_delete'),
    
    # other plant func
    path('category_plants/<str:category>', CategoryPlantView.as_view(),
        name='category_plants'),
    path('latin_plants/<str:latin_title>', LatinNamePlantView.as_view(),
        name='latin_plants'),
    path('favorites_plants/<int:pk>', FavoritesPlantView.as_view(), 
        name='favorites_plants'),
    path('most_liked/', MostLikedPlantView.as_view(), 
        name='most_liked_plants'),
    path('most_viewed/', MostViewedPlantView.as_view(), 
        name='most_viewed_plants'),
    
    path('plant_like/<slug:slug>/', PlantLike, name='plant_like'),
    path('plant_favorites/<slug:slug>', AddFavorites, name='add_plant_favorites'),
]
