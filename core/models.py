from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.

class Profile(AbstractUser):
    PROFILE_TYPE_CHOICES = [
        ("D", "Doador"),
        ("P", "Ponto de Coleta")
    ]
    email = models.EmailField(unique=True, 
            error_messages={'unique': "Já existe um usuário com este email", 'required': 'Por favor dgite um email'})
    profile_type = models.CharField(max_length=1, choices=PROFILE_TYPE_CHOICES)
    phone = models.CharField(max_length=11)
    about = models.TextField(max_length=300)
    img_profile = models.ImageField(upload_to='img_profile', null=True, blank=True)


class Donnor(Profile):
    cpf = models.CharField(max_length=11, unique=True, error_messages={'unique': "Já existe outro usuário com esse CPF"})
    ranking_points = models.PositiveIntegerField(default=0)
    general_points = models.PositiveIntegerField(default=0)


class Place(models.Model):
    parent_company = models.CharField(max_length=100, verbose_name="Sede")
    place_name = models.CharField(max_length=100, verbose_name="Logradouro")
    number = models.CharField(max_length=10, verbose_name="Número")
    district = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=100, verbose_name="Estado")
    complement = models.CharField(max_length=200, null=True, blank=True, verbose_name="Complemento")


class RecyclingCenter(Profile):
    cnpj = models.CharField(max_length=14, unique=True, error_messages={'unique': 'Já existe outro usuário com esse CNPJ'})
    place = models.OneToOneField(Place, on_delete=CASCADE, null=True, blank=True)


class Donation(models.Model):
    donor_id = models.ForeignKey(Donnor, on_delete=CASCADE)
    recyclingCenter_id = models.ForeignKey(RecyclingCenter, on_delete=CASCADE)
    description = models.TextField(max_length=300, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=None)
    added_points = models.PositiveIntegerField(default=0)


class RecyclabelMaterial(models.Model):
    donation_id = models.ForeignKey(Donation, on_delete=CASCADE)
    material_name = models.CharField(max_length=100)
    quatity = models.PositiveIntegerField()
    

