from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, PlayerProfileForm
from .models import User, PlayerProfile, RefereeProfile


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'events:home'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create profile based on user type
            if user.user_type == 'player':
                PlayerProfile.objects.create(user=user)
            else:
                RefereeProfile.objects.create(user=user)

            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('events:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    profile = None

    if user.user_type == 'player':
        profile, created = PlayerProfile.objects.get_or_create(user=user)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile
    })


@login_required
def profile_edit(request):
    user = request.user
    profile = None

    if user.user_type == 'player':
        profile, created = PlayerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = PlayerProfileForm(request.POST, instance=profile) if profile else None

        if user_form.is_valid() and (not profile_form or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = PlayerProfileForm(instance=profile) if profile else None

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class PlayerDirectoryView(ListView):
    model = User
    template_name = 'accounts/player_directory.html'
    context_object_name = 'players'
    paginate_by = 12

    def get_queryset(self):
        return User.objects.filter(user_type='player').select_related('player_profile')
