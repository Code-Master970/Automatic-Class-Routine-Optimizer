from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def Home(request):
    return render(request, "index.html")

def About(request):
    return render(request, "about.html")

def Schedule(request):
    return render(request, "schedule.html")


@login_required(login_url='/signup_or_login/')
def Today_schedule(request):
    return render(request, "today schedule.html")

