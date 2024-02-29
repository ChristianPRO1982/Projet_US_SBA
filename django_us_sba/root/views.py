from django.shortcuts import render, redirect

def root_homepage(request):
    return render(request, 'root/root_homepage.html')

def signup(request):
    return render(request, 'root/signup.html')
