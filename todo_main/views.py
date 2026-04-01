from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from todo.models import Task


# 🔐 Home page (Login required)
@login_required
def home(request):
    # ✅ Show only current user's tasks
    tasks = Task.objects.filter(
        user=request.user,
        is_completed=False
    ).order_by('-updated_at')

    completed_tasks = Task.objects.filter(
        user=request.user,
        is_completed=True
    )

    context = {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'home.html', context)