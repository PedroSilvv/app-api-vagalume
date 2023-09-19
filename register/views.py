from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth import login as login_user
from django.contrib import messages
import re


def pw_validation(password):

    if len(password) < 6:
        return False

    if not re.search("[!@#$%^&*()_+-={}|\\:;\"\'<>,.?/]", password):
        return False

    if not re.search("\d", password):
        return False

    if not re.search("[A-Z]", password):
        return False

    if not re.search("[a-z]", password):
        return False

    return True



def register(request):

    if request.method == 'GET':

        return render(request, 'register.html')

    else:

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        secpass = request.POST.get('password2')


        if password == secpass:
                if pw_validation(password):

                    if User.objects.filter(username=username).exists():
                        messages.error(request, "Nome de usuário ja em uso!")
                        return redirect('register')
                    else:

                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        login_user(request, user)
                        return render(request, "home.html")

                else:
                    messages.error(request, f"A senha precisa ter 6 caracteres, conter letras maisculas, minusculas\n"
                                            f"e caractéres especiais.")
                    return redirect('register')

        else:
            messages.error(request, "As senhas não conferem.")
            return redirect('register')



