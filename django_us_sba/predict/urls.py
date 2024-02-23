from django.urls import path
from predict import views

urlpatterns = [
    path('', views.homepage, name='root_homepage'),
]
