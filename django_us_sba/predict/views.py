from django.shortcuts import render

def predict_homepage(request):
    return render(request, 'predict/predict_homepage.html')