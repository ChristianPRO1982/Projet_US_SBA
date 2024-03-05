from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def predict_homepage(request):
    return render(request, 'predict/predict_homepage.html')

@login_required
def new_process(request):
    return render(request, 'predict/new_process.html')