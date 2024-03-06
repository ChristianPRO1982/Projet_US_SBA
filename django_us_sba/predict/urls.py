from django.urls import path
from predict import views

urlpatterns = [
    path('', views.predict_homepage, name='predict_homepage'),
    path('<int:pk>/', views.SelectProcess.as_view(), name="func-select_process"),
    path('new_process/', views.new_process, name='new_process'),
    path('process_location/', views.process_location, name='process_location'),
    path('process_bank/', views.process_bank, name='process_bank'),
    path('process_activity/', views.process_activity, name='process_activity'),
    path('process_bankloan/', views.process_bankloan, name='process_bankloan'),
    path('process_guaranteedamountrequested/', views.process_guaranteedamountrequested, name='process_guaranteedamountrequested'),
    path('process_sbaapprouval/', views.process_sbaapprouval, name='process_sbaapprouval'),
]
