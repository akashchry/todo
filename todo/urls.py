from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # 🏠 Dashboard
    path('', views.home, name='home'),   # 🔥 better: homepage instead of /home/

    # 📝 Task CRUD
    path('task/add/', views.add_task, name='add_task'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),

    # ✅ Task Status
    path('task/<int:pk>/done/', views.mark_as_done, name='mark_as_done'),
    path('task/<int:pk>/undone/', views.mark_as_undone, name='mark_as_undone'),
    
]