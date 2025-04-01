from django import forms
from .models import ItemComanda, Comanda
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ItemComandaForm(forms.ModelForm):
    class Meta:
        model=ItemComanda
        fields=['produs','cantitate']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PlasareComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['metoda_plata', 'metoda_livrare']

class FinalizareComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['metoda_plata', 'metoda_livrare']