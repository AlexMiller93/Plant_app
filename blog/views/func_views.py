from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post, Comment


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
