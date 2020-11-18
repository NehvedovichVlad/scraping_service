from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from accounts.forms import UserLoginForm, UserRegisterForm, UserUpdateForm

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    """checks if the user is registered"""
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                return redirect('home')
            
        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language, 
                     'send_email': user.send_email}
        )
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
    return redirect('home')