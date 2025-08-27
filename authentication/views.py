from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.conf import settings

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", {"form": form})

