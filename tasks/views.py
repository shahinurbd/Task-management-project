from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome Home</h1>")

def contact(request):
    return HttpResponse("This is contact page")

def showtask(request):
    return HttpResponse("This is our task page")



    

