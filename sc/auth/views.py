from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password'] 
        name = request.POST['name'] 

        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required!')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('signup')

        try:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )
            user.save()


            auth_login(request, user)
            messages.success(request, 'Registration successful! Welcome aboard!')
            return redirect('home')  

        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html') 
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        if not email or not password:
            messages.error(request, 'Both email and password are required!')
            return redirect('login')

        try:
            user = User.objects.filter(email=email).first()
            if user:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    auth_login(request, user)
                    # messages.success(request, 'Login successful!')
                    return redirect('home')  
                else:
                    messages.error(request, 'Invalid credentials!')
            else:
                messages.error(request, 'No account found with this email!')

        except Exception as e:
            print(messages)
            messages.error(request, f'An error occurred during login: {str(e)}')

        return redirect('login')

    return render(request, 'login.html')  

def logout(request):
    auth_logout(request)
    # messages.success(request, 'Logged out successfully!')
    return redirect('login')
