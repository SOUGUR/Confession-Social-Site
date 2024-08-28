# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages 

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