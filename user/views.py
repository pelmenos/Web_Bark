from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.info(request, 'Пароли не совпадают')
            return redirect('/')
        elif User.objects.filter(username=username):
            messages.info(request, 'Это имя уже используется!')
            return redirect('/')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, 'Вы зарегестрировались!')
            return redirect('/')


def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Неверный логин или пароль')
            return redirect('/')


def Logout(request):
    logout(request)
    request.user = None
    return redirect('/')
