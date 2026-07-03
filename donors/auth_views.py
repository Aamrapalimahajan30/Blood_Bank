from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.authtoken.models import Token


def hospital_signup(request):
    if request.user.is_authenticated:
        return redirect('camp_listing')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        hospital_name = request.POST.get('hospital_name', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'donors/hospital_signup.html')
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'donors/hospital_signup.html')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'donors/hospital_signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'donors/hospital_signup.html')

        user = User.objects.create_user(username=username, password=password,first_name=hospital_name)
        user.is_staff = True
        user.is_active = False
        user.save()
        Token.objects.create(user=user)

        messages.success(
            request,
            'Account created! A BloodBank admin needs to approve your hospital '
            'account before you can log in. You will be notified once approved.'
        )
        return redirect('login')

    return render(request, 'donors/hospital_signup.html')


def hospital_login(request):
    if request.user.is_authenticated:
        return redirect('camp_listing')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('camp_listing')

        
        unapproved = User.objects.filter(username=username, is_active=False).exists()
        if unapproved:
            messages.warning(request, 'Your hospital account is still pending admin approval.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'donors/hospital_login.html')


def hospital_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def my_api_token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'donors/api_token.html', {'token': token.key})