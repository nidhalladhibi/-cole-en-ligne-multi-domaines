from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

# -----------------------------
# Register
# -----------------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # <-- get بدل []
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not password or not password2:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('register')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

# -----------------------------
# Login
# -----------------------------
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # <-- استخدم get بدل []
        password = request.POST.get('password')  # <-- لتجنب الخطأ إذا الحقل غير موجود
        if not username or not password:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe invalide.')
            return redirect('login')
    return render(request, 'accounts/login.html')

# -----------------------------
# Logout
# -----------------------------
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# -----------------------------
# Profile
# -----------------------------
@login_required
def profile(request):
    # التأكد من وجود Profile
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Votre profil a été mis à jour!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)
