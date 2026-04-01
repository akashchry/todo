from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from accounts.views import dashboard_redirect


# 🔐 Redirect root → login page
def root_redirect(request):
    return redirect('login')


urlpatterns = [
    # 🔹 Admin panel
    path('admin/', admin.site.urls),

    # 🔹 Default route → login
    path('', root_redirect, name='root'),

    # 🔐 Authentication URLs
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # 🔐 Signup (accounts app)
    path('accounts/', include('accounts.urls')),

    # 📌 Todo app (home page inside this)
    path('todo/', include('todo.urls')),

    path('dashboard/', dashboard_redirect, name='dashboard'),
]