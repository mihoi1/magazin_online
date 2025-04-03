from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
import re

from .cos import *
from .comanda import *
from .user import *


def lista_produse(request):
    query = request.GET.get('q', '')
    produse = Produs.objects.filter(denumire__icontains=query) if query else Produs.objects.all()
    return render(request, 'online_store/lista_produse.html', {'produse': produse, 'query': query})

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    form = ItemComandaForm()
    return render(request, 'online_store/detalii_produs.html', {'produs': produs, 'form': form})

@login_required
def procesare_plata(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, user=request.user, status='in_asteptare')

    if request.method == "POST":
        nume_pe_card = request.POST.get("nume_pe_card", "").strip()
        numar_card = request.POST.get("numar_card", "").replace(" ", "")
        cvv = request.POST.get("cvv", "")

        if not nume_pe_card:
            error = "Numele de pe card este obligatoriu."
        elif not re.fullmatch(r"\d{16}", numar_card):
            error = "Numărul cardului trebuie să conțină exact 16 cifre."
        elif not re.fullmatch(r"\d{3}", cvv):
            error = "CVV-ul trebuie să aibă exact 3 cifre."
        else:
            # Simulam confirmarea platii
            comanda.status = "plasata"
            comanda.save()
            return redirect('pagina_confirmare_comanda')

        return render(request, 'online_store/procesare_plata.html', {'comanda': comanda, 'error': error})

    return render(request, 'online_store/procesare_plata.html', {'comanda': comanda})

@login_required
def cont_utilizator(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'online_store/cont_utilizator.html', context)