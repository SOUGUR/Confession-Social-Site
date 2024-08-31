# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PostForm
from django.contrib import messages 
from .models import Post, Like


def start(request):
    return render(request, "accounts/start.html")

def aboutus(request):
    return render(request, "accounts/aboutus.html")


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        # Get the password and password confirmation from the form
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # Check if passwords match
        if password and password_confirm and password != password_confirm:
            form.add_error('password_confirm', "Passwords do not match.")  # Add error to the form

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)  # Use the plain password
            user.save()
            messages.success(request, "Registration successful! Please log in.")  # Add a success message
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def postconfession(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False, user=request.user)
            post.save()
            return redirect('viewpost') 
    else:
        form = PostForm()

    return render(request, 'post_confessionform.html', {'form': form})

@login_required
def view_post(request):
    posts = Post.objects.order_by('-created_at')
    # Add a flag to each post indicating if the current user has liked it
    for post in posts:
        post.is_liked_by_user = post.like_set.filter(user=request.user).exists()

    return render(request, 'post_list.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
    
    return redirect('viewpost')  


