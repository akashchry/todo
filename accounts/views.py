from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from todo.models import Task


# 📝 Signup View (Improved)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # 🔥 Auto login after signup
            login(request, user)

            # 🔁 Redirect based on role
            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


# 🔀 Role-Based Redirect
@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')   # 🧑‍💻 admin
    else:
        return redirect('home')              # 👤 user


# 🧑‍💻 Admin Dashboard
@login_required
def admin_dashboard(request):
    users = User.objects.all()
    tasks = Task.objects.all()

    return render(request, 'accounts/admin_dashboard.html', {
        'users': users,
        'tasks': tasks
    })