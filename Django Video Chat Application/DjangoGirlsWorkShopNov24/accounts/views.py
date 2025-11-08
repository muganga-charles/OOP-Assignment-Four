"""
BONUS FEATURE: Authentication Views
Handles user registration, login, profile management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserProfile, OnlineUser
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm


def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('chat:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('chat:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Mark user as online
            user.profile.is_online = True
            user.profile.save()
            
            # Track online session
            OnlineUser.objects.get_or_create(
                user=user,
                session_key=request.session.session_key
            )
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('chat:index')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """User logout"""
    # Mark user as offline
    request.user.profile.is_online = False
    request.user.profile.save()
    
    # Remove online session
    OnlineUser.objects.filter(user=request.user).delete()
    
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """View user profile"""
    profile = request.user.profile
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def user_list_view(request):
    """BONUS: List all users with search"""
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
    else:
        users = User.objects.exclude(id=request.user.id)
    
    online_users = UserProfile.objects.filter(is_online=True)
    
    context = {
        'users': users,
        'online_users': online_users,
        'query': query
    }
    return render(request, 'accounts/user_list.html', context)


@login_required
def user_detail_view(request, username):
    """View another user's profile"""
    user = User.objects.get(username=username)
    profile = user.profile
    
    context = {
        'profile_user': user,
        'profile': profile
    }
    return render(request, 'accounts/user_detail.html', context)