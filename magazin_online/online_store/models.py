from django.db import models
from django.contrib.auth.models import User

class Produs(models.Model):
    denumire = models.CharField(max_length=100)
    descriere=models.TextField()
    pret=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products/')
 
    class Meta:
        verbose_name_plural='Produse'
    
    def __str__(self):
        return self.denumire
    
class Comanda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_plasare = models.DateTimeField(auto_now_add=True)
    pret_total=models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural='Comenzi'

    def __str__(self):
        return f"Comanda {self.id} plasata de {self.user.username}"
    
class ItemComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural='Iteme_Comanda'

    def __str__(self):
        return f"{self.cantitate} x {self.produs.denumire}"