from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView)

from .models import Post
from .forms import PostForm, PostEditForm

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class PostCreateView(CreateView):
    model = Post
    form_class= PostForm
    template_name = "blog/post_create.html"

class PostUpdateView(UpdateView):
    model = Post
    form_class= PostEditForm
    template_name = 'blog/post_update.html'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')