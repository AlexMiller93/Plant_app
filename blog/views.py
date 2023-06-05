from itertools import chain
from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView)
from django.utils.text import slugify
from .models import Post, Comment
from users.models import Profile
from .forms import PostForm, PostEditForm, CommentForm, CommentEditForm

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = Profile.objects.order_by('-created_on')
        
        # profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        # followers = Profile.objects.filter(followed_by = profile)
        # posts = Post.objects.filter(
        #     author__in=followers).order_by('-created_on')
        posts = Post.objects.all().order_by('-created_on')
        tags = [post.tag for post in posts]
        unique_tags = list(set(tags))
        context["tags"] = unique_tags
        
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/crud/post_detail.html"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        # working with likes
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['post_is_liked'] = liked
        
        # who seen post
        if self.request.user.is_authenticated:
            post.seen_by.add(self.request.user)
        
        # noted functionality
        
        # share post functionality
        # profile = Profile.object.get(pk=request.user.profile.id)
        
        
        # *** working with comments *** 
        comments = Comment.objects.filter(post=self.get_object(), reply=None)
        replies = Comment.objects.exclude(post=self.get_object(), reply=None)
        
        data['comments'] = comments
        data['replies'] = replies
        data['comment_form'] = CommentForm()
        return data
    
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.method == 'POST':
                
                '''
                # user who follows or unfollow
                current_user = request.user.profile
                # post of author which user want to follow/unfollow
                post = get_object_or_404(Post, slug=self.kwargs['slug'])
                # find profile of user which is post author
                profile = Profile.objects.get(user=post.author.user)
                try:
                    action = request.POST['follow']
                    if action == "Unfollow":
                        current_user.follows.remove(profile)
                    elif action == "Follow":
                        current_user.follows.add(profile)
                    current_user.save()
                except:
                    return redirect(self.request.path_info)
                '''
                
                
                comment_form = CommentForm(self.request.POST)
                if comment_form.is_valid():
                    content = comment_form.cleaned_data['content']
                    reply = comment_form.cleaned_data['reply']
                    if content:
                        # normal comment
                        if not reply:
                            new_comment = Comment(
                                content=content, 
                                author = self.request.user.profile, 
                                post=self.get_object()).save()
                            
                        # reply
                        else:
                            new_comment = Comment(
                                content=content, 
                                author = self.request.user.profile, 
                                post=self.get_object(), reply=reply).save()
                    else:
                        messages.warning(request, 'You post empty comment. Write something ...')
                return redirect(self.request.path_info)
            else:
                comment_form = CommentForm()
                return redirect(self.request.path_info)
        else:
            messages.warning(request, 'Your should login to write comment or reply')
            return redirect(self.request.path_info)
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class= PostForm
    template_name = "blog/crud/post_create.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
    
    # def get_success_url(self):
    #     return redirect('home')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class= PostEditForm
    template_name = 'blog/crud/post_update.html'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/crud/post_delete.html'
    success_url = reverse_lazy('home')
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.all()
        return Post.objects.filter(author=self.request.user.profile)
    
    # def test_func(self):
    #     post = get_object_or_404(Post, slug=self.kwargs['slug'])
    #     if self.request.user.profile == post.author:
    #         return True
    #     return False

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/posts/user_post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = get_object_or_404(Profile, 
            id=self.kwargs['pk'])
        followers = Profile.objects.filter(followed_by = profile)
        
        user_posts = Post.objects.filter(
            author__id = profile.id)
        shared_posts = Post.objects.filter(
            share = profile)
        feed_posts = Post.objects.filter(
            author__in=followers)
        
        all_posts = list(chain(user_posts, shared_posts, feed_posts))
        context["profile"] = profile
        context["user_posts"] = all_posts
        return context

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/posts/tag_post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs['tag']
        tag_posts = Post.objects.filter(tag=tag).order_by('-created_on')
        context["tag_posts"] = tag_posts
        context["tag"] = tag
        return context
    
class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/posts/search_post_list.html'

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

class OneStatusPostListView(ListView):
    model = Post
    template_name = 'blog/posts/status_post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.kwargs['status']
        
        profiles = Profile.objects.filter(user_status = status)
        status_posts = Post.objects.filter(author__in = profiles).order_by('-created_on')
        
        context["status_posts"] = status_posts
        context["status"] = status
        return context
    
class FavoritesPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/posts/favorites_post_list.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        data["favor_posts"] = Post.objects.filter(favorites=profile)
        return data

class MostLikedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/posts/most_liked.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["most_liked_posts"] = Post.objects.annotate(
                like_count=Count('likes')).order_by('-like_count')
        return data
    
class MostCommentedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/posts/most_commented.html'
    paginate_by = 3
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["most_commented_posts"] = Post.objects.annotate(
                comment_count=Count('comments')).order_by('-comment_count')
        return data
    
class ChangeOrderPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.order_by('created_on')
        context["posts"] = posts
        return context

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']  # What needs to appear in the page for update
    template_name = 'blog/comment/comment_update.html'  # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        comment = get_object_or_404(Comment, post=post, pk=self.kwargs['pk'])
        data['post'] = post
        data['comment'] = comment
        return data
    
    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = Post.objects.get(slug=self.object.post.slug)
        return post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment/comment_confirm_delete.html'  # <app>/<model>_<viewtype>.html
    
    def get_success_url(self):
        post = Post.objects.get(slug=self.object.post.slug)
        return post.get_absolute_url()
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user.profile == comment.author or self.request.user.is_superuser:
            return True
        return False
    
@login_required
def PostLike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.profile.id).exists():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def CommentLike(request, slug, pk):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, post=post, pk=pk)
    
    if comment.likes.filter(id=request.user.profile.id).exists():
        comment.likes.remove(request.user.profile)
    else:
        comment.likes.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def AddFavorites(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.profile != post.author:
        if post.favorites.filter(id=request.user.profile.id).exists():
            post.favorites.remove(request.user.profile)
        else:
            post.favorites.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def SharePost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.profile != post.author:
        if post.share.filter(id=request.user.profile.id).exists():
            post.share.remove(request.user.profile)
        else:
            post.share.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))

    
    
# https://www.youtube.com/watch?v=PXqRPqDjDgc