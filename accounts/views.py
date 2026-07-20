from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Create the user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('profile')

    else:

        form = ProfileForm(instance=profile)

    return render(
        request,
        'profile.html',
        {
            'profile': profile,
            'form': form
        }
    )

@login_required(login_url='login')
def user_profile(request, username):

    user = get_object_or_404(User, username=username)

    profile = user.profile

    posts = user.post_set.all().order_by('-created_at')

    is_following = request.user in profile.followers.all()

    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }

    return render(
        request,
        'user_profile.html',
        context
    )

@login_required(login_url='login')
def follow_user(request, username):

    if request.method == "POST":

        user = get_object_or_404(User, username=username)

        profile = user.profile

        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)

    return redirect('user_profile', username=username)

@login_required(login_url='login')
def users_list(request):

    profiles = Profile.objects.all()

    context = {
        'profiles': profiles
    }

    return render(
        request,
        'users_list.html',
        context
    )