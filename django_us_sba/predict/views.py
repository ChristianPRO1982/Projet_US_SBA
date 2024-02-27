from django.shortcuts import render

def predict_homepage(request):
    return render(request, 'html/predict_homepage.html')