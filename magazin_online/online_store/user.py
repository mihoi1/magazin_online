from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import Http404, HttpResponse
from online_store.models import Comanda
from online_store.forms import RegisterForm, LoginForm

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('lista_produse')
    else:
        form=RegisterForm()
    return render(request, 'online_store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)
         if user is not None:
             login(request,user)
             return redirect('lista_produse')
        else:
            return render(request, 'online_store/login.html', {'form': form})
    else:
        form=LoginForm()
    return render(request, 'online_store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('lista_produse')