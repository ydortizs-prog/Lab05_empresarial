from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request, 'core/landing.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def perfil(request):
    return render(request, 'users/perfil.html')