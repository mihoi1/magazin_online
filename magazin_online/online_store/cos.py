from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import Http404, HttpResponse
from online_store.models import Comanda, ItemComanda, Produs

@login_required
def adauga_in_cos(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    comanda, created = Comanda.objects.get_or_create(user=request.user, status='in_asteptare')

    # Verificam daca produsul exista deja in cos
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