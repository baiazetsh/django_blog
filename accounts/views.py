from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)  # Автоматический вход
            messages.success(request, f'Welcome, {new_user.username}! You have been logged in.')
            return redirect('blogs:index')  # Перенаправляем на главную
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)