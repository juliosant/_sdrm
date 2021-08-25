from django import forms
from .models import Attending, Donation, Donnor, Place, Profile, RecyclabelMaterial, RecyclingCenter
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    user = forms.CharField(label="Usuário:", widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuario'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'placeholder': "Digite sua senha"}))


class RegisterDonorForm(UserCreationForm):
    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Telefone')
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


class RegisterDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'


class RegisterMaterialForm(forms.ModelForm):
    class Meta:
        model = RecyclabelMaterial
        fields = '__all__'
        widgets = {
            'material_name': forms.TextInput(attrs={'required':'',  'pattern':"[A-Za-z0-9]{1,100}"}),
            'quatity': forms.NumberInput(attrs={'onclick': 'calculator();', 'required':'','pattern':'[^0-9]\d+'}), 
        }


class SearchDonorForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Digite ID, nome ou sobrenome de alguém...'}))


class SearchRecyclingCenterForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Pesquise por um ponto de coleta...'}))


class AttendanceForm(forms.ModelForm):
    #place = forms.CharField(max_length=200)
    class Meta:
        model = Attending
        fields = '__all__'
        widgets = {
            'place': forms.TextInput(attrs={'readonly': ''}),
            
        }
        