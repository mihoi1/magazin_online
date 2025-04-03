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
    STATUS_CHOICES = (
        ('in_asteptare', 'În asteptare'),
        ('plasata', 'Plasată'),
        ('livrata', 'Livrată'),
        ('anulata', 'Anulată'),
    )
    METODE_PLATA = [
        ('card', 'Card bancar'),
        ('ramburs', 'Plată la livrare'),
    ]

    METODE_LIVRARE = [
        ('curier', 'Curier rapid'),
        ('easybox', 'Easybox'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_plasare = models.DateTimeField(auto_now_add=True)
    pret_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_asteptare')
    metoda_plata = models.CharField(max_length=20, choices=METODE_PLATA, default='card')
    metoda_livrare = models.CharField(max_length=20, choices=METODE_LIVRARE, default='curier')

    class Meta:
        verbose_name_plural = 'Comenzi'

    def calculeaza_pret_total(self):
        total = sum(item.produs.pret * item.cantitate for item in self.itemcomanda_set.all())
        self.pret_total = total
        self.save()

    def __str__(self):
        return f"Comanda {self.id} - {self.user.username} - {self.status}"
    
class ItemComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural='Iteme_Comanda'

    def __str__(self):
        return f"{self.cantitate} x {self.produs.denumire}"