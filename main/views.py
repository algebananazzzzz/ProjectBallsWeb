from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import signupForm
from .models import User


def home(request):
    return render(request=request, template_name="main/home.html")


def login(request):
    form_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # messages.info(request, f"Hello, {username}")
                return redirect("/dashboard")
        else:
            form_message = "Invalid username or password."
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"form_message": form_message})


def logout(request):
    auth.logout(request)
    return redirect("/")


def signup(request):
    error_message = None
    if request.method == 'POST':

        form = signupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=raw_password)
            auth.login(request, user)

            return redirect('/dashboard')

        else:
            error_message = "Username already exists. Login instead?"

    return render(request=request, template_name="main/signup.html", context={'error_message': error_message})


def dashboard(request):
    return render(request=request, template_name="main/dashboard.html")


def board(request):
    return render(request=request, template_name="main/board.html")


def snippets(request):
    return render(request=request, template_name="main/snippets.html")


def configure(request, boardPk=None):
    if request.method == "POST":
        for i in request.POST:
            print(i, request.POST[i])
    return render(request=request, template_name="main/configure.html", context={'boardPk': 1})
# Create your views here.
