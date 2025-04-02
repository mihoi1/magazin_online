from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produse, name='lista_produse'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('produs/<int:produs_id>/', views.detalii_produs, name='detalii_produs'),
    path('adauga-in-cos/<int:produs_id>', views.adauga_in_cos, name="adauga_in_cos"),
    path('cos/', views.cos, name='cos'),
    path('cont/', views.cont_utilizator, name='cont_utilizator'),
    path('finalizare-comanda/', views.finalizare_comanda, name='finalizare_comanda'),
    path('sterge-din-cos/<int:item_id>/', views.sterge_din_cos, name='sterge_din_cos'),
    path('istoric-comenzi/', views.istoric_comenzi, name='istoric_comenzi'),
    path('admin/comenzi/<int:comanda_id>/status/', views.actualizeaza_status_comanda, name='actualizeaza_status_comanda'),
    path('confirmare-comanda/', views.pagina_confirmare_comanda, name='pagina_confirmare_comanda'),
    path('procesare-plata/<int:comanda_id>/', views.procesare_plata, name='procesare_plata'),
    path('comanda/<int:comanda_id>/', views.detalii_comanda, name='detalii_comanda'),
]
