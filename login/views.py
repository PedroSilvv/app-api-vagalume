from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login(request):

    if request.method == "GET":

        return render(request, "login.html")

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            login_user(request, user)
            return render(request, "home.html")

        else:
            messages.error(request, "O usuário ou a senha estão errado.")
            return redirect('login')


def log_out(request):
    logout(request)

    return redirect('homepage')




