from django.shortcuts import render


def home(request):
    return render(request, "example_project/home.html")


def other(request):
    return render(request, "example_project/other.html")
