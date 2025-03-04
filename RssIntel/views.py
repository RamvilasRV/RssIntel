from django.shortcuts import render, redirect

def home(request):
	username = request.user.username
	return render(request, "home.html", {"username":username})