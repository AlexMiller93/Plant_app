from itertools import chain
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.models import Profile

from .forms import CommentForm, PostEditForm, PostForm
from .models import Comment, Post


# Create your views here.

class HomeView(ListView):
    """ For rendering all posts, users and tags on main page
        Pagination works correctly.

    Returns:
        dict: dict context with keys - profiles and tags
    """

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.order_by('-created_on')
        context["profiles"] = profiles

        posts = Post.objects.values_list('tag', flat=True).distinct().order_by('-created_on')
        context["tags"] = posts
        return context


class PostDetailView(DetailView):
    """ For rendering one post for your pk, 
        - to calculate quantity of comments, replies
        - to write comment under the post
        - to write reply under comment
        - to like current post

    Returns:
        dict: dict data with keys - post_is_liked, 
        comments, replies, comment_form
    """

    model = Post
    template_name = "blog/crud/post_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # post like system
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        liked = self.request.user.id in post.likes.values_list('id', flat=True)
        data['post_is_liked'] = liked

        # who have been seen the post
        if self.request.user.is_authenticated:
            post.seen_by.add(self.request.user)

        # calculate quantity of comments and replies
        comments = Comment.objects.filter(post=self.get_object(), reply=None)
        replies = Comment.objects.exclude(post=self.get_object(), reply=None)

        data['comments'] = comments
        data['replies'] = replies
        data['comment_form'] = CommentForm()
        return data

    # write comment or reply
    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(request, 'You should login to write comment or reply')
            return redirect(self.request.path_info)

        if self.request.method != 'POST':
            return redirect(self.request.path_info)

        comment_form = CommentForm(self.request.POST)
        if not comment_form.is_valid():
            return redirect(self.request.path_info)

        content = comment_form.cleaned_data['content']
        reply = comment_form.cleaned_data['reply']

        if not content:
            messages.warning(request, 'You posted an empty comment. Write something ...')
            return redirect(self.request.path_info)

        new_comment = Comment(
            content=content,
            author=self.request.user.profile,
            post=self.get_object()
        )

        if reply:
            new_comment.reply = reply

        new_comment.save()

        return redirect(self.request.path_info)


class PostCreateView(LoginRequiredMixin, CreateView):
    """ Create post. 
        User should be authorized. Post's author will be current user.  
    """

    model = Post
    form_class = PostForm
    template_name = "blog/crud/post_create.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """ Update post. User should be authorized.  """

    model = Post
    form_class = PostEditForm
    template_name = 'blog/crud/post_update.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """ Delete post. User should be authorized.  """

    model = Post
    template_name = 'blog/crud/post_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.all()
        return Post.objects.filter(author=self.request.user.profile)


class UserPostListView(ListView):
    """ For rendering user posts for your pk which includes:
        - own posts
        - shared posts (can't share own posts)
        - posts of follows

    Returns:
        dict: dict context with keys - profile and user_posts
    """

    model = Post
    template_name = 'blog/posts/user_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        followers = Profile.objects.filter(followed_by=profile)

        user_posts = Post.objects.filter(author__id=profile.id)
        shared_posts = Post.objects.filter(share=profile)
        feed_posts = Post.objects.filter(author__in=followers)

        all_posts = list(chain(user_posts, shared_posts, feed_posts))

        context.update({
            "profile": profile,
            "user_posts": all_posts
        })

        return context


class TagPostListView(ListView):
    """ For rendering posts with certain tag

    Returns:
        dict: dict context with keys - tag and tag_posts
    """

    model = Post
    template_name = 'blog/posts/tag_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs['tag']
        context["tag_posts"] = Post.objects.filter(tag=tag).order_by('-created_on')
        context["tag"] = tag
        return context


class SearchPostListView(ListView):
    """ For rendering posts which found for certain search request
    User can find for plant title, plant tag, plant content
    

    Returns:
        dict: dict context with keys - query and posts
    """

    model = Post
    template_name = 'blog/posts/search_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        posts = self.model.objects.filter(
            Q(content__icontains=query) |
            Q(title__icontains=query) |
            Q(tag__icontains=query)).order_by('-created_on') if query else self.model.objects.none()

        context["query"] = query
        context["posts"] = posts
        return context


class OneStatusPostListView(ListView):
    """ For rendering posts from users with certain user status

    Returns:
        dict: dict context with keys - status and status_posts
    """

    model = Post
    template_name = 'blog/posts/status_post_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = self.kwargs['status']

        profiles = Profile.objects.filter(user_status=status)
        status_posts = Post.objects.filter(author__in=profiles).order_by('-created_on')

        context["status_posts"] = status_posts
        context["status"] = status
        return context


class FavoritesPostListView(LoginRequiredMixin, ListView):
    """ For rendering favorites user posts.
    User should be authorized.


    Returns:
        dict: dict data with keys - favor_posts
    """

    model = Post
    template_name = 'blog/posts/favorites_post_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        favor_posts = Post.objects.filter(favorites=profile)
        data.update({"favor_posts": favor_posts})
        return data


class MostLikedPostListView(LoginRequiredMixin, ListView):
    """ For rendering most liked posts. 
        User should be authorized.

    Returns:
        dict: dict data with key most_liked_posts
    """

    model = Post
    template_name = 'blog/posts/most_liked.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        most_liked_posts = Post.objects.annotate(
            like_count=Count('likes')).order_by('-like_count')
        data = super().get_context_data(**kwargs)
        data["most_liked_posts"] = most_liked_posts
        return data


class MostCommentedPostListView(LoginRequiredMixin, ListView):
    """ For rendering most commented posts. 
        User should be authorized.

    Returns:
        dict: dict data with key most_commented_posts
    """

    model = Post
    template_name = 'blog/posts/most_commented.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        most_commented_posts = Post.objects.annotate(
            comment_count=Count('comments')).order_by('-comment_count')
        data = super().get_context_data(**kwargs)
        data["most_commented_posts"] = most_commented_posts
        return data


class MostViewPostListView(LoginRequiredMixin, ListView):
    """ For rendering most visited posts. 
        User should be authorized.

    Returns:
        dict: dict data with key most_visited_posts
    """

    model = Post
    template_name = 'blog/posts/most_visited.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        most_visited_posts = Post.objects.annotate(
            view_count=Count('seen_by')).order_by('-view_count')
        data = super().get_context_data(**kwargs)
        data["most_visited_posts"] = most_visited_posts
        return data


class ChangeOrderPostListView(ListView):
    """ For rendering with reverse order posts.

    Returns:
        dict: dict context with keys - favor_posts
    """

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.order_by('created_on')
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """ For edit comment.
    Redirects after checking form
    User should be authorized.

    Args:
        LoginRequiredMixin (_type_): _description_
        UpdateView (_type_): _description_

    Returns:
        dict: dict data with keys - post and comment
    """

    model = Comment
    fields = ['content']
    template_name = 'blog/comment/comment_update.html'  # <app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        comment = get_object_or_404(Comment, post=post, pk=self.kwargs['pk'])
        return {
            'post': post,
            'comment': comment,
            **super().get_context_data(**kwargs)
        }

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = Post.objects.get(slug=self.object.post.slug)
        return post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ For delete comment.  
    User should be authorized.

    Returns:
        dict: dict data with keys - post and comment
    """

    model = Comment
    template_name = 'blog/comment/comment_confirm_delete.html'  # <app>/<model>_<viewtype>.html

    def get_success_url(self):
        post = Post.objects.get(slug=self.object.post.slug)
        return post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        if self.request.user.profile == comment.author:
            return True
        return False


@login_required
def post_like(request, slug):
    """
    Like or unlike a post based on the user's preference.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the post to be liked or unliked.

    Returns:
        HttpResponseRedirect: Redirects the user back to the previous page.
    """

    post = get_object_or_404(Post, slug=slug)
    is_liked = post.likes.filter(id=request.user.profile.id).exists()

    if is_liked:
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def comment_like(request, slug, pk):
    """ Like comment post from certain slug """

    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, post=post, pk=pk)

    profile_id = request.user.profile.id
    likes = comment.likes
    if profile_id in likes.values_list('id', flat=True):
        likes.remove(request.user.profile)
    else:
        likes.add(request.user.profile)
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def add_favorites(request, slug):
    """ Add post from certain slug to favorites  """

    post = get_object_or_404(Post, slug=slug)
    user_profile = request.user.profile
    favorites = post.favorites

    if user_profile != post.author:
        if user_profile.id in favorites:
            favorites.remove(user_profile)
        else:
            favorites.add(user_profile)
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def share_post(request, slug):
    """ To share post from certain slug """

    post = get_object_or_404(Post, slug=slug)
    user_profile = request.user.profile

    if user_profile != post.author:
        if post.share.filter(id=user_profile.id).exists():
            post.share.remove(user_profile)
        else:
            post.share.add(user_profile)
    return redirect(request.META.get("HTTP_REFERER"))
