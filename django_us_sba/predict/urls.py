from django.urls import path
from predict import views

urlpatterns = [
    path('', views.predict_homepage, name='predict_homepage'),
    path('new_process/', views.new_process, name='new_process'),
]
