from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addTask, name='addTask'),
]
