from django import forms
from .models import Donnor, Place, Profile, RecyclingCenter
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    user = forms.CharField(label="Usuário:", widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuario'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'placeholder': "Digite sua senha"}))


class RegisterDonorForm(UserCreationForm):
    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(label='Email')
    profile_type = forms.ChoiceField(choices=Profile.PROFILE_TYPE_CHOICES)
    cpf = forms.CharField(label='CPF', max_length=11)

    class Meta:
        model = Donnor
        fields = ['first_name', 'last_name','email', 'profile_type', 'cpf', 'username', 'password1', 'password2']


class RegisterRecyclingForm(UserCreationForm):
    first_name = forms.CharField(label="Razão Social")
    last_name = forms.CharField(label='Nome Fantasia')
    email = forms.EmailField(label='Email')
    profile_type = forms.ChoiceField(choices=Profile.PROFILE_TYPE_CHOICES)
    cnpj = forms.CharField(label='CNPJ', max_length=14)

    class Meta:
        model = RecyclingCenter
        fields = ['first_name', 'last_name', 'email', 'profile_type', 'cnpj', 'username', 'password1', 'password2']


class RegisterPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'