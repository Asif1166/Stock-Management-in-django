from django.shortcuts import render, redirect
from .forms import CustomSignupForm, CustomLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.




def registration(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                # Check if a user with the same username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken.')
                else:
                    # Create the new user and save to the database
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    messages.success(
                        request, 'Account created successfully. You can now login.')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
    else:
        form = CustomSignupForm()
    return render(request, 'screens/registration.html', {'form': form})




def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If user is authenticated, log them in
                login(request, user)
                # Replace 'home' with your desired redirect URL
                return redirect('home')
            else:
                # If user is not authenticated, show an error message
                print(form.errors)
    else:
        form = CustomLoginForm()
    return render(request, 'screens/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')
