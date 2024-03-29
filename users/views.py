import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView

from blog.views.func_views import is_ajax
from .forms import ProfileForm, UserForm, SignUpForm
from .models import Profile
from blog.models import Post, Comment


# Create your views here.

class SignUpView(CreateView):
    """ Create a new user account  """

    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"

    """
    
    def get(self, request, **kwargs):
        user_form = SignUpForm()
        return render(
            request, 'registration/register.html',
            {'user_form': user_form}
        )

    def post(self, request, **kwargs):
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            return render(
                request, 'registration/register_done.html',
                {'new_user': new_user}
            )
    """


class ProfileView(LoginRequiredMixin, DetailView):
    """ For render profile page. User should be authorized.
    Current user can follow or unfollow user from profile page.

    Returns:
        dict: dict context with keys - profile, posts, 
            shared_posts, comments and replies
    """

    model = Profile
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs: object) -> object:
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])

        posts = Post.objects.filter(author=profile)
        shared_posts = Post.objects.filter(share=profile)
        comments = Comment.objects.filter(author=profile).exclude(reply=None)
        replies = Comment.objects.filter(author=profile)

        context.update({
            'profile': profile,
            'posts': posts,
            'shared_posts': shared_posts,
            'comments': comments,
            'replies': replies
        })
        return context

    # to follow, unfollow 
    def post(self, request, pk):
        current_user = request.user.profile

        # profile_id = self.kwargs['pk']
        profile = get_object_or_404(Profile, id=pk)
        action = request.POST['follow']

        # if action == "Unfollow":
        #     #     current_user.follows.remove(profile)
        #     follow = UserFollowing.objects.get(user_id=current_user, following_user_id=profile)
        #     follow.delete()
        #
        # elif action == "Follow":
        #     #     current_user.follows.add(profile)
        #     UserFollowing.objects.create(user_id=current_user, following_user_id=profile)

        current_user.save()

        return redirect(request.META.get("HTTP_REFERER"))


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """ Update profile settings. User should be authorized.

    Returns:
        dict: dict context with keys - user_from and profile_form
    """

    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'users/profile_update.html'

    def get(self, request: object, *args: object, **kwargs: object) -> object:
        return self.post(request)

    # when post new data - use post method
    def post(self, request: object) -> object:
        post_data = request.POST or None
        file_data = request.FILES or None
        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('home'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)
        return self.render_to_response(context)


@require_POST
@login_required
def toggle_follow(request):
    if request.method == "POST" and is_ajax(request):
        profile_id = request.POST.get('profile_id', None)
        profile_to_follow = get_object_or_404(Profile, pk=profile_id)
        user_profile = request.user

        if profile_to_follow.followers.filter(id=user_profile.id).exists():
            profile_to_follow.followers.remove(user_profile)
            is_following = False
        else:
            profile_to_follow.followers.add(user_profile)
            is_following = True

        data = {
            'profile_id': profile_id,
            'is_following': is_following,
        }

        return HttpResponse(json.dumps(data), content_type='application/json')
