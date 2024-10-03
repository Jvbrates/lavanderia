from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def view_test(request):
    return render(request, "test.html")

def login(request):
    return render(request, "login.html")