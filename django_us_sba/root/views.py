from django.shortcuts import render, redirect

def root_homepage(request):
    return render(request, 'html/root_homepage.html')

def signup(request):
    return render(request, 'html/signup.html')
