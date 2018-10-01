from django.shortcuts import render


def home(request):
    data = {"title": "Home", "home": "active"}
    return render(request, "home.html", data)
