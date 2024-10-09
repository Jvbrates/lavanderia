from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect
import typing


@login_required
def view_test(request):
    return render(request, "test.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login", permanent=True)
