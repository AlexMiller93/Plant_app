from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
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
class UserFeedPlantsView(ListView):
    """ For rendering plants from user followers

    Returns:
        dict: dict data with key feed_plants
    """

    model = Plant
    template_name = 'plants/list/follow_plants.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])

        followers = Profile.objects.filter(followed_by=profile)
        feed_plants = Plant.objects.filter(owner__in=followers).order_by('-created_on')
        data["feed_plants"] = feed_plants
        return data


class UserPlantsView(ListView):
    """ For rendering plants from certain user 

    Returns:
        dict: dict data with key user_plants
    """

    model = Plant
    template_name = 'plants/list/user_plants.html'
    context_object_name = 'plants'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        user_plants = Plant.objects.filter(owner=profile).order_by('-created_on')
        data["user_plants"] = user_plants
        return data


class PlantDetailView(DetailView):
    """ For rendering plant info with certain slug.
    When user visited plant view increase.
    
    Returns:
        dict: dict data with key plant
    """

    model = Plant
    template_name = 'plants/crud/plant_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        plant = get_object_or_404(Plant, slug=self.kwargs['slug'])

        # who seen plant
        if self.request.user.is_authenticated:
            plant.seen_by.add(self.request.user)

        context["plant"] = plant
        return context


class PlantCreateView(LoginRequiredMixin, CreateView):
    """ Add a new plant. User should be authorized.  """

    model = Plant
    form_class = PlantForm
    template_name = 'plants/crud/plant_add.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class PlantUpdateView(LoginRequiredMixin, UpdateView):
    """ For update user plant. User should be authorized.  """

    model = Plant
    form_class = PlantEditForm
    template_name = 'plants/crud/plant_update.html'


class PlantDeleteView(LoginRequiredMixin, DeleteView):
    """
        For delete user plant. User should be authorized.
    """

    model = Plant
    template_name = 'plants/crud/plant_delete.html'
    success_url = reverse_lazy('home')


class CategoryPlantView(ListView):
    """ For rendering plants with certain category. 

    Returns:
        dict: dict context with keys - category and category_plants
    """

    model = Plant
    template_name = 'plants/list/category_plant_list.html'

    def get_context_data(self, **kwargs):
        category = self.kwargs['category']
        category_plants = Plant.objects.filter(category=category).order_by('-created_on')
        context = super().get_context_data(**kwargs)
        context.update({"category_plants": category_plants, "category": category})
        return context


class LatinNamePlantView(ListView):
    """ For rendering plants with certain latin name. 

    Returns:
        dict: dict context with keys - latin_title and latin_plants
    """

    model = Plant
    template_name = 'plants/list/latin_plant_list.html'

    def get_context_data(self, **kwargs):
        latin_title = self.kwargs['latin_title']
        latin_plants = Plant.objects.filter(latin_title=latin_title).order_by('-created_on')
        context = super().get_context_data(**kwargs)
        context.update({"latin_title": latin_title}, {"latin_plants": latin_plants})
        return context


class MostLikedPlantView(LoginRequiredMixin, ListView):
    """ For rendering most liked plants. 
        User should be authorized.

    Returns:
        dict: dict data with key most_liked_plants
    """

    model = Plant
    template_name = 'plants/list/most_liked.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        most_liked_plants = Plant.objects.annotate(
            like_count=Count('plant_like')).order_by('-like_count')
        return {"most_liked_plants": most_liked_plants}


class MostViewedPlantView(LoginRequiredMixin, ListView):
    """ For rendering most visited plants. 
        User should be authorized.

    Returns:
        dict: dict data with key most_viewed_plants
    """

    model = Plant
    template_name = 'plants/list/most_viewed.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        most_viewed_plants = Plant.objects.annotate(
            view_count=Count('seen_by')).order_by('-view_count')
        return {"most_viewed_plants": most_viewed_plants}


class FavoritesPlantView(LoginRequiredMixin, ListView):
    """ For rendering user favorites plants . 
        User should be authorized.

    Returns:
        dict: dict data with key favor_plants
    """

    model = Plant
    template_name = 'plants/list/favorites_plant_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        favor_plants = Plant.objects.filter(fav_plants=profile)
        return {"favor_plants": favor_plants}


@login_required
def plant_like(request, slug):
    """ Like plant with certain slug  """

    plant = get_object_or_404(Plant, slug=slug)
    if plant.likes.filter(id=request.user.profile.id).exists():
        plant.likes.remove(request.user.profile)
    else:
        plant.likes.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def add_favorites(request, slug):
    """  Add plant to user's favorites  """

    plant = get_object_or_404(Plant, slug=slug)
    user_profile = request.user.profile
    if user_profile != plant.owner:
        if plant.fav_plants.filter(id=user_profile.id).exists():
            plant.fav_plants.remove(user_profile)
        else:
            plant.fav_plants.add(user_profile)
    return redirect(request.META.get("HTTP_REFERER"))
