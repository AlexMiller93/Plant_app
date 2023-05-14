from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView)

from .models import Plant
from users.models import Profile
from .forms import PlantForm, PlantEditForm

# Create your views here.
class PlantsView(ListView):
    model = Plant
    template_name = 'plants/all_plants.html'

class UserPlantsView(ListView):
    model = Plant
    template_name = 'plants/user_plants.html'
    context_object_name = 'plants'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, 
            id=self.kwargs['pk'])
        user_plants = Plant.objects.filter(owner=profile).order_by('-created_on')
        data["user_plants"] = user_plants
        return data

class PlantDetailView(DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        plant = get_object_or_404(Plant, slug=self.kwargs['slug'])
        context["plant"] = plant
        return context

class PlantCreateView(LoginRequiredMixin, CreateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_add.html'
    success_url = reverse_lazy('home')

    def form_valid(self, request, form):
        form.instance.owner = self.request.user.profile
        messages.success(request, 'You add plant! Wow!!')
        return super().form_valid(form)
    
class PlantUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant
    form_class = PlantEditForm
    template_name = 'plants/plant_update.html'

class PlantDeleteView(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = 'plants/plant_delete.html'
    success_url = reverse_lazy('home')

class CategoryPlantView(ListView):
    pass

class LatinNamePlantView(ListView):
    pass

class MostLikedPlantView(LoginRequiredMixin, ListView):
    pass

class FavoritesPlantView(LoginRequiredMixin, ListView):
    pass

@login_required
def PlantLike(request):
    pass

@login_required
def AddFavorites(request):
    pass
