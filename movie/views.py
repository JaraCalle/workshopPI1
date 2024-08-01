from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "home.html", {'name': 'Juan José Jara Calle'})

def about(request):
    return render(request, "about.html")