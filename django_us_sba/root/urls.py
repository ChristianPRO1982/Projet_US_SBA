from django.urls import path
from root import views

urlpatterns = [
    path('', views.homepage, name='root_homepage'),
]
