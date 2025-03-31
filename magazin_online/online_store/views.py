from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404


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
    comanda, created = Comanda.objects.get_or_create(user=request.user, status='in_asteptare')

    # Verificăm dacă produsul există deja în coș
    item, item_created = ItemComanda.objects.get_or_create(comanda=comanda, produs=produs)
    if not item_created:
        item.cantitate += 1
        item.save()

    comanda.calculeaza_pret_total()
    
    return redirect('cos')

@login_required
def cos(request):
    comanda = Comanda.objects.filter(user=request.user, status='in_asteptare').first()
    return render(request, 'online_store/cos.html', {'comanda': comanda})

@login_required
def finalizeaza_comanda(request):
    comanda = Comanda.objects.filter(user=request.user, status='in_cos').first()
    if comanda:
        comanda.status = 'plasata'
        comanda.save()
        # Aici poți adăuga trimiterea unui email de confirmare
    return redirect('istoric_comenzi')

def lista_produse(request):
    query = request.GET.get('q', '')
    produse = Produs.objects.filter(denumire__icontains=query) if query else Produs.objects.all()
    return render(request, 'online_store/lista_produse.html', {'produse': produse, 'query': query})

@login_required
def sterge_din_cos(request, item_id):
    item = get_object_or_404(ItemComanda, id=item_id)

    comanda = item.comanda
    item.delete()

    # Recalculează prețul total după ștergere
    if comanda.itemcomanda_set.exists():
        comanda.calculeaza_pret_total()
    else:
        comanda.pret_total = 0
        comanda.save()

    return redirect('cos')    

@login_required
def procesare_plata(request):
    comanda = Comanda.objects.filter(user=request.user, status='in_cos').first()
    if not comanda:
        return redirect('cos')

    if request.method == "POST":
        # Simulăm procesarea plății
        comanda.status = 'plasata'
        comanda.save()
        return redirect('istoric_comenzi')

    return render(request, 'online_store/procesare_plata.html', {'comanda': comanda})

@login_required
def cont_utilizator(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'online_store/cont_utilizator.html', context)

@login_required
def istoric_comenzi(request):
    comenzi = Comanda.objects.filter(user=request.user).order_by('-data_plasare')
    return render(request, 'online_store/istoric_comenzi.html', {'comenzi': comenzi})

@staff_member_required
def actualizeaza_status_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    
    if request.method == 'POST':
        comanda.status = request.POST['status']
        comanda.save()
        return redirect('admin_comenzi')

    return render(request, 'online_store/actualizeaza_status.html', {'comanda': comanda})   

@login_required
def finalizare_comanda(request):
    comanda = Comanda.objects.filter(user=request.user, status='in_asteptare').first()
    
    if not comanda or not comanda.itemcomanda_set.exists():
        return redirect('cos')

    if request.method == 'POST':
        comanda.metoda_plata = request.POST['metoda_plata']
        comanda.metoda_livrare = request.POST['metoda_livrare']
        comanda.status = 'in_asteptare'
        comanda.pret_total = sum(item.produs.pret * item.cantitate for item in comanda.itemcomanda_set.all())
        comanda.save()

        return redirect('istoric_comenzi')

    return render(request, 'online_store/finalizare_comanda.html', {'comanda': comanda})