from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, DeleteView

from blog.models import Comment, Post


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