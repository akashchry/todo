from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now
from .models import Task


# 🔐 LOGIN
def user_login(request):
    if request.user.is_authenticated:
        return redirect('todo:home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "All fields are required ❌")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.username} 🎉")
            return redirect('todo:home')

        messages.error(request, "Invalid username or password ❌")
        return redirect('login')

    return render(request, 'login.html')


# 📝 SIGNUP
def signup(request):
    if request.user.is_authenticated:
        return redirect('todo:home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([username, email, password]):
            messages.error(request, "All fields are required ❌")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ⚠")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered ⚠")
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully 🎉")
        return redirect('login')

    return render(request, 'signup.html')


# 🚪 LOGOUT
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully 👋")
    return redirect('login')


# 🏠 DASHBOARD (🔥 CLEAN + OPTIMIZED)
@login_required
def home(request):
    query = request.GET.get('q', '').strip()
    priority = request.GET.get('priority', '')
    filter_type = request.GET.get('filter', 'all')

    tasks = Task.objects.filter(user=request.user)

    # 🔍 Search
    if query:
        tasks = tasks.filter(task__icontains=query)

    # 🎯 Priority filter
    if priority:
        tasks = tasks.filter(priority=priority)

    today = now().date()

    # 📊 Groups
    pending_tasks = tasks.filter(is_completed=False)
    completed_tasks = tasks.filter(is_completed=True)

    overdue_tasks = pending_tasks.filter(due_date__lt=today)
    today_tasks = pending_tasks.filter(due_date=today)

    # 🔥 Filter logic
    filter_map = {
        'pending': pending_tasks,
        'completed': completed_tasks,
        'overdue': overdue_tasks,
        'today': today_tasks,
        'all': tasks
    }

    display_tasks = filter_map.get(filter_type, tasks)

    context = {
        'tasks': display_tasks.order_by('-created_at'),

        # 📊 Dashboard counts
        'total_tasks': tasks.count(),
        'completed_count': completed_tasks.count(),   # ✅ YOUR REQUIRED CHANGE
        'pending_count': pending_tasks.count(),
        'overdue_count': overdue_tasks.count(),
        'today_count': today_tasks.count(),

        # 🔎 Filters
        'query': query,
        'priority': priority,
        'filter_type': filter_type,
        'today': today,
    }

    return render(request, 'home.html', context)


# ➕ ADD TASK
@login_required
def add_task(request):
    if request.method == 'POST':
        task_text = request.POST.get('task', '').strip()
        priority = request.POST.get('priority', 'Medium')
        due_date = request.POST.get('due_date') or None

        if not task_text:
            messages.error(request, "Task cannot be empty ❌")
            return redirect('todo:home')

        Task.objects.create(
            user=request.user,
            task=task_text,
            priority=priority,
            due_date=due_date
        )

        messages.success(request, "Task added successfully ✅")

    return redirect('todo:home')


# ✔ MARK DONE
@login_required
def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if not task.is_completed:
        task.is_completed = True
        task.save(update_fields=['is_completed'])
        messages.success(request, "Task marked as done ✔")

    return redirect('todo:home')


# ↩ MARK UNDONE
@login_required
def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if task.is_completed:
        task.is_completed = False
        task.save(update_fields=['is_completed'])
        messages.info(request, "Task moved back ↩")

    return redirect('todo:home')


# ✏ EDIT TASK
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task_text = request.POST.get('task', '').strip()
        priority = request.POST.get('priority', 'Medium')
        due_date = request.POST.get('due_date') or None

        if not task_text:
            messages.error(request, "Task cannot be empty ❌")
            return redirect('todo:edit_task', pk=pk)

        task.task = task_text
        task.priority = priority
        task.due_date = due_date
        task.save()

        messages.success(request, "Task updated ✏")
        return redirect('todo:home')

    return render(request, 'edit_task.html', {'task': task})


# 🗑 DELETE TASK
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    task.delete()
    messages.warning(request, "Task deleted 🗑")

    return redirect('todo:home')