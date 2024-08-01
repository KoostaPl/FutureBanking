from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from authuser.models import User
from authuser.forms import UserRegisterForm

def RegisterUserView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Client {username} has been registered successfully!')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("account:account")
        
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("account:account")
    
    else:
        form = UserRegisterForm()
    context = {
        "form" : form
    }
    return render(request, "sign-up.html", context)

def LoginUserView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged!")
                return redirect("account:account")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("authuser:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("account:account")
    return render(request, "sign-in.html")

def LogoutUserView(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("authuser:sign-in")