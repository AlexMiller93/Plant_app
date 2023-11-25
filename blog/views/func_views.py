try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blog.models import Post, Comment


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


@login_required
@require_POST
def like_post(request):
    if request.method == "POST" and is_ajax(request):
        post_id = request.POST.get('post_id', None)
        post = get_object_or_404(Post, pk=post_id)

        if post.likes.filter(id=request.user.profile.id).exists():
            post.likes.remove(request.user.profile)
            liked = False
        else:
            post.likes.add(request.user.profile)
            liked = True

        data = {
            'post_id': post_id,
            'liked': liked,
            'total_likes': post.likes.count()
        }
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@login_required
@require_POST
def post_like(request):
    """
    Like or unlike a post based on the user's preference.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the post to be liked or unliked.

    Returns:
        HttpResponseRedirect: Redirects the user back to the previous page.
    """
    post_id = request.POST.get('id', None)
    post = get_object_or_404(Post, id=post_id)

    # Check if the user liked the post
    user_liked = request.user in post.likes.all()  # True/ False

    if user_liked:
        post.likes.remove(request.user)
        user_liked = False  # The user now no longer likes the post
    else:
        post.likes.add(request.user)
        user_liked = True  # The user now likes the post

    return JsonResponse({'likes': post.likes.count(), 'user_liked': user_liked})


@login_required
@require_POST
def like_comment(request):
    if request.method == "POST" and is_ajax(request):
        comment_id = request.POST.get('comment_id', None)
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.likes.filter(id=request.user.profile.id).exists():
            comment.likes.remove(request.user.profile)
            liked = False
        else:
            comment.likes.add(request.user.profile)
            liked = True

        data = {
            'comment_id': comment_id,
            'liked': liked,
            'total_likes': comment.likes.count()
        }
        return HttpResponse(json.dumps(data), content_type='application/json')


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

