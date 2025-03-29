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
    path('cont/', views.cont_utilizator, name='cont_utilizator')
]
