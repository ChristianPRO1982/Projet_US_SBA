from django.shortcuts import render

def root_homepage(request):
    return render(request, 'html/root_homepage.html')