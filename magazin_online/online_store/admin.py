from django.contrib import admin
from .models import *

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display=('denumire', 'pret')
    search_fields=('denumire',)
    list_filter=('pret',)

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display=('user_username','pret_total','data_plasare')
    search_fields=('user__username',)
    list_filter=('pret_total','data_plasare',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description='User'

@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display=('comanda__id', 'produs__denumire', 'cantitate')
    search_fields=('produs__denumire',)
    list_filter=('cantitate',)