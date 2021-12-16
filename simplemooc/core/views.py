from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

# Create your views here.
