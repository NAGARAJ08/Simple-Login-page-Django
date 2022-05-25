from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from discuss import settings

# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['psw']
        Rpassword = request.POST['psw-repeat']

        if User.objects.filter(username=username):
            messages.error(request, "User Already exits")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already in use")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Must be within 10 characters")

        if password != Rpassword:
            messages.error(request, "Passwords did not match")

        if not username.isalnum():
            messages.error(request, "User name must be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, "Account Successfully Created.  we have sent confirmation email please verify!!")



        return redirect('/signin')
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        psw = request.POST['psw']

        user = authenticate(username=username, password=psw)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, "authentication/index.html", {'firstname': firstname})
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')
