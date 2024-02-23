from django.urls import path
from predict import views

urlpatterns = [
    path('', views.homepage, name='predict_homepage'),
]
