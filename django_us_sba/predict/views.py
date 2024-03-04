from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def predict_homepage(request):
    return render(request, 'predict/predict_homepage.html')