from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from users.forms import CustomRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
        
            messages.success(request,"Registration Successful")
            return redirect('sign-up')
        
    return render(request, 'registations/register.html', {"form": form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registations/login.html')

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')

