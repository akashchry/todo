from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # ✅ THIS FIXES /todo/

    path('add/', views.addTask, name='addTask'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('mark-done/<int:pk>/', views.mark_as_done, name='mark_as_done'),
    path('mark-undone/<int:pk>/', views.mark_as_undone, name='mark_as_undone'),
]