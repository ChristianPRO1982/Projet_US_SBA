from django.urls import path
from root import views

urlpatterns = [
    path('', views.root_homepage, name='root_homepage'),
    path('signup', views.signup, name='signup'),
]
