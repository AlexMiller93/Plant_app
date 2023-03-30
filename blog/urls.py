from django.urls import path
from django.views.generic.base import TemplateView
# from .views import HomePageView

urlpatterns = [
    path('', TemplateView.as_view(template_name="blog/home.html"), name='home'),
]