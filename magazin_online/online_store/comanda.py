from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from online_store.models import Comanda, ItemComanda

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
    
    if not comanda:
        return render(request, 'online_store/finalizare_comanda.html', {'error': "Nu ai produse în coș sau comanda a fost deja plasată."})

    if request.method == "POST":
        metoda_plata = request.POST.get("metoda_plata")
        metoda_livrare = request.POST.get("metoda_livrare")
        
        if not metoda_plata or not metoda_livrare:
            return render(request, 'online_store/finalizare_comanda.html', {"comanda": comanda, "error": "Te rog să selectezi metoda de plată și livrare."})

        # Salvăm metoda de plată și livrare
        comanda.metoda_plata = metoda_plata
        comanda.metoda_livrare = metoda_livrare

        if metoda_plata == "ramburs":
            # Plata la livrare -> marcăm direct ca platită
            comanda.status = "plasata"
            comanda.save()
            return redirect('pagina_confirmare_comanda')
        else:
            # Plata cu cardul -> simulăm procesul de plată
            return redirect('procesare_plata', comanda_id=comanda.id)

    return render(request, 'online_store/finalizare_comanda.html', {"comanda": comanda})

def pagina_confirmare_comanda(request):
    return render(request, 'online_store/confirmare_comanda.html')

def detalii_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    produse = ItemComanda.objects.filter(comanda=comanda)  # Obținem produsele din comanda

    return render(request, 'online_store/detalii_comanda.html', {
        'comanda': comanda,
        'produse': produse
    })