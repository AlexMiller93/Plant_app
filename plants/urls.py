from django.urls import path

from .views import (
    PlantsView,
    UserPlantsView,
    PlantDetailView,
    PlantCreateView,
    PlantUpdateView,
    PlantDeleteView,
    
)

urlpatterns = [
    path('', PlantsView.as_view(), name="all_plants"),
    path('/<int:pk>', UserPlantsView.as_view(), 
        name="user_plants"),
    path('/<slug:slug>', PlantDetailView.as_view(),
        name="plant_detail"),
    
    # CRUD for plants
    path('/add', PlantCreateView.as_view(), 
        name='plant_add'),
    path('/edit/<slug:slug>/', PlantUpdateView.as_view(), 
        name='plant_edit'),
    path('/delete/<slug:slug>/', PlantDeleteView.as_view(), 
        name='plant_delete'),
    
]
