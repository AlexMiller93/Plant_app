from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView)
from django.utils.text import slugify

from .models import Post
from users.models import Profile
from .forms import PostForm, PostEditForm

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = Profile.objects.order_by('-created_on')
        
        tags = [post.tag for post in Post.objects.all()]
        unique_tags = list(set(tags))
        context["tags"] = unique_tags
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        post_for_like = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if post_for_like.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = post_for_like.likes.count()
        data['post_is_liked'] = liked
        return data
    
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class= PostForm
    template_name = "blog/post_create.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class= PostEditForm
    template_name = 'blog/post_update.html'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post_list.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, 
            id=self.kwargs['pk'])
        context["profile"] = profile
        context["user_posts"] = Post.objects.filter(
            author__id = profile.id).order_by('-created_on')
        return context
    
class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_post_list.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs['tag']
        tag_posts = Post.objects.filter(tag=tag).order_by('-created_on')
        context["tag_posts"] = tag_posts
        context["tag"] = tag
        return context
    
class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/search_post_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            posts = self.model.objects.filter(
                Q(content__icontains=query) | 
                Q(title__icontains=query) | 
                Q(tag__icontains=query)).order_by('-created_on')
            
        else:
            posts = self.model.objects.none()
        context["query"] = query
        context["posts"] = posts
        return context

def PostLike(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.profile.id).exists():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)
        
    return redirect('post_detail', slug=post.slug)
    # return HttpResponseRedirect(reverse('post_detail'), args=[slug])

# https://www.youtube.com/watch?v=PXqRPqDjDgc