from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm, LoginForm
from .models import Profile
from django.contrib.auth.models import User

def register_step1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('register_step2')
    else:
        form = UserRegisterForm()
    return render(request, 'cuentas/register.html', {'form': form})

@login_required
def register_step2(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, '¡Tu perfil ha sido completado con éxito! 🎉')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'cuentas/register_step2.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'cuentas/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'cuentas/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'cuentas/home.html')

@login_required
def profile_list(request):
    perfiles = Profile.objects.select_related('user').all()
    return render(request, 'cuentas/profile_list.html', {'perfiles': perfiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'cuentas/profile_detail.html', {'profile': profile})