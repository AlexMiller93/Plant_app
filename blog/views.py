from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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
        
        posts = Post.objects.all()
        tags = [post.tag for post in posts]
        unique_tags = list(set(tags))
        context["tags"] = unique_tags
        
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        # working with likes
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = post.likes.count()
        data['post_is_liked'] = liked
        
        # who seen post
        if self.request.user.is_authenticated:
            post.seen_by.add(self.request.user)
        
        # noted functionality
        
        
        # *** working with comments *** 
        
        # retrieve list of comments excluding replies
        comments = Comment.objects.filter(post=self.get_object(), reply=None)
        all_comments = Comment.objects.filter(post=self.get_object())
        replies_count = sum(map(lambda x: not x.is_parent, all_comments))
        
        data['comments'] = comments
        data['comments_count'] = comments.count()
        data['replies_count'] = replies_count
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
    template_name = 'blog/status_post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # status = self.kwargs['status']
        # # profiles = Profile.objects.filter(user_status = status)
        # # for profile in profiles: 
        # status_posts = Post.objects.filter(author.profile.user_status=status).order_by('-created_on')
        # context["status_posts"] = status_posts
        # context["status"] = status
        return context

def PostLike(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.profile.id).exists():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)
        
    return redirect('post_detail', slug=post.slug)

def PostNote(request, slug):
    post_noted = request.GET.get('post_noted', False)
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    
    try:
        post.post_noted = post_noted
        post.save()
        return JsonResponse({"noted": True})
    except Exception as e:
        return JsonResponse({"noted": False})
    return JsonResponse(data)
    
    

# https://www.youtube.com/watch?v=PXqRPqDjDgc