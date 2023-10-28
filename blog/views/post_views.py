from itertools import chain
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from taggit.models import Tag

from users.models import Profile
from ..forms import CommentForm, PostEditForm, PostForm
from ..models import Comment, Post


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

        # TODO: do backend to show for unique tags
        # posts = Post.objects.values_list('tags', flat=True).distinct().order_by('-created_on')

        posts = Post.objects.all()  # all posts in db
        # tags = Tag.objects.all() # all tags in Tag model
        # tags = [post.tags for post in posts]
        # tags = list(set(tags))
        # tags = Tag.objects.filter(post__in=posts).distinct()
        tags = Tag.objects.filter(post__id__in=posts).distinct()

        context["profiles"] = profiles
        context["tags"] = tags
        context["posts"] = posts
        return context

    def get_context(self, request):
        context = super(HomeView, self).get_context(request)

        blog_content_type = ContentType.objects.get_for_model(Post)
        tags = Tag.objects.filter(
            taggit_taggeditem_items__content_type=blog_content_type
        )
        context["tags"] = tags
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
        comments = post.comments.all()
        # comments = Comment.objects.filter(post=self.get_object(), reply=None)
        replies = Comment.objects.exclude(post=self.get_object(), reply=None)

        # find similar posts
        # if post.tags:
        post_tags_id = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_id).exclude(id=post.id)
        similar_posts = similar_posts.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-created_on')[:3]

        data.update({
            'comments': comments,
            'replies': replies,
            'comment_form': CommentForm(),
            'similar_posts': similar_posts,

        })
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
        # form.save_m2m()
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
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        tags_posts = Post.objects.filter(tags=tag)
        context.update({
            'tag': tag,
            'tag_posts': tags_posts
        })
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

        """
        
        # -- search against multiple fields
        posts = self.model.objects.annotate(
            search=SearchVector('content', 'title'),
                ).filter(search=query).order_by('-created_on')
        
        # -- stemming and ranking search
        search_vector = SearchVector('content', 'title')
        search_query = SearchQuery(query)
        
        posts = self.model.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
                ).filter(search=search_query).order_by('-rank')
                
        # -- weighting queries
        search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
        search_query = SearchQuery(query)
        posts = self.model.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.2).order_by('-rank')
        
        """

        # search with trigram similarity
        posts = self.model.objects.annotate(
            similarity=TrigramSimilarity('title', query),
        ).filter(similarity__gt=0.2).order_by('similarity')

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
