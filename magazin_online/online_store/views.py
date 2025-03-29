from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

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

def lista_produse(request):
    produse = Produs.objects.all()
    return render(request, 'online_store/lista_produse.html', {'produse': produse})

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    form = ItemComandaForm()
    return render(request, 'online_store/detalii_produs.html', {'produs': produs, 'form': form})

@login_required
def adauga_in_cos(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    comanda, creata = Comanda.objects.get_or_create(user=request.user)
    form = ItemComandaForm(request.POST)
    if form.is_valid():
        item_comanda = form.save(commit=False)
        item_comanda.comanda = comanda
        item_comanda.produs = produs
        item_comanda.save()
    return redirect('cos')

@login_required
def cos(request):
    comanda = Comanda.objects.filter(user=request.user).first()
    return render(request, 'online_store/cos.html', {'comanda': comanda})

@login_required
def cont_utilizator(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'online_store/cont_utilizator.html', context)