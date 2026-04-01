from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user, is_completed=False)
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True)

    return render(request, 'home.html', {
        'tasks': tasks,
        'completed_tasks': completed_tasks
    })


@login_required
def addTask(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        if task_text:
            Task.objects.create(
                user=request.user,
                task=task_text,
                priority=priority,
                due_date=due_date
            )

    return redirect('home')


@login_required
def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('home')


@login_required
def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = False
    task.save()
    return redirect('home')


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('home')


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.task = request.POST.get('task')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('home')

    return render(request, 'edit_task.html', {'task': task})