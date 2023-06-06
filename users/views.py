from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.detail import DetailView

from .forms import ProfileForm, UserForm
from .models import Profile
from blog.models import Post, Comment

# Create your views here.

class SignUpView(CreateView):
    """ Create a new user account  """
    
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"
    
class ProfileView(LoginRequiredMixin, DetailView):
    """ For render profile page. User should be authorized.
    Current user can follow or unfollow user from profile page.

    Returns:
        dict: dict context with keys - profile, posts, 
            shared_posts, comments and replies
    """
    
    model = Profile
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        
        posts = Post.objects.filter(author=profile)
        shared_posts = Post.objects.filter(share=profile)
        comments = Comment.objects.filter(author=profile).exclude(reply=None)
        replies = Comment.objects.filter(author=profile)
        
        context['profile'] = profile
        context['posts'] = posts
        context['shared_posts'] = shared_posts
        context['comments'] = comments
        context['replies'] = replies
        return context
    
    # to follow, unfollow 
    def post(self, request, **kwargs):
        current_user = request.user.profile
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        action = request.POST['follow']
        if action == "Unfollow":
            current_user.follows.remove(profile)
        elif action == "Follow":
            current_user.follows.add(profile)
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
    
    def get(self, request, *args, **kwargs):
        return self.post(request)
    
    # when post new data - use post method
    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None
        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('home'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

