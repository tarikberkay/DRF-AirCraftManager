from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse


def register(request):
    return render(request, "auth/register.html")


def login(request):
    return render(request, "auth/login.html")



@login_required
def dashboard(request):
    return render(request, "hub/dashboard.html")


@login_required
def index(request):
    return render(request, "index.html")













# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# def register(request):
#     return render(request, "auth/register.html")


# def login(request):
#     return render(request, "auth/login.html")


# @login_required
# def dashboard(request):
#     return render(request, "hub/dashboard.html")


# @login_required
# def index(request):
#     return render(request, "index.html")
