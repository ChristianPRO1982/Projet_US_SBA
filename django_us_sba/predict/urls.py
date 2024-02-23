from django.urls import path
from predict import views

urlpatterns = [
    path('', views.predict_index, name='predict_homepage'),
]
