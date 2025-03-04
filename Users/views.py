from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import UserRegisterForm


# Create your views here.
def UserRegistrationView(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Your account is registerd")
			return redirect("home")
	else:
		form = UserRegisterForm()
	return render(request, "registration/register.html", {"form":form})