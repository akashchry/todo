from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task


@login_required
def home(request):
    query = request.GET.get('q')
    priority = request.GET.get('priority')

    tasks = Task.objects.filter(user=request.user, is_completed=False).order_by('-created_at')
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).order_by('-created_at')

    # 🔍 Search
    if query:
        tasks = tasks.filter(task__icontains=query)
        completed_tasks = completed_tasks.filter(task__icontains=query)

    # 🎯 Priority filter
    if priority:
        tasks = tasks.filter(priority=priority)

    context = {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'query': query,
        'priority': priority
    }

    return render(request, 'home.html', context)


@login_required
def addTask(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        priority = request.POST.get('priority') or 'Medium'
        due_date = request.POST.get('due_date')

        if task_text:
            Task.objects.create(
                user=request.user,
                task=task_text,
                priority=priority,
                due_date=due_date if due_date else None
            )
            messages.success(request, "Task added successfully ✅")

    return redirect('home')


@login_required
def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = True
    task.save()
    messages.success(request, "Task marked as done ✔")
    return redirect('home')


@login_required
def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = False
    task.save()
    messages.info(request, "Task moved back ↩")
    return redirect('home')


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.error(request, "Task deleted 🗑")
    return redirect('home')


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.task = request.POST.get('task')
        task.priority = request.POST.get('priority') or 'Medium'
        due_date = request.POST.get('due_date')

        task.due_date = due_date if due_date else None
        task.save()

        messages.success(request, "Task updated successfully ✏")
        return redirect('home')

    return render(request, 'edit_task.html', {'task': task})