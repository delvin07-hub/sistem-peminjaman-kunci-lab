from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Selamat datang, ' + user.username)
            return redirect('dashboard')
        messages.error(request, 'Username atau password salah!')
    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Anda telah logout.')
    return redirect('login')
