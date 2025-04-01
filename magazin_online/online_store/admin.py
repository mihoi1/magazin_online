from django.contrib import admin
from .models import *

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display=('denumire', 'pret')
    search_fields=('denumire',)
    list_filter=('pret',)

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_plasare', 'pret_total', 'status', 'metoda_plata', 'metoda_livrare')
    list_filter = ('status', 'metoda_plata', 'metoda_livrare')
    search_fields = ('user__username',)
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description='User'

@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display=('comanda__id', 'produs__denumire', 'cantitate')
    search_fields=('produs__denumire',)
    list_filter=('cantitate',)

