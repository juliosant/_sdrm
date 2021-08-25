from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey, OneToOneField

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


class Donnor(Profile): # Donor
    cpf = models.CharField(max_length=11, unique=True, error_messages={'unique': "Já existe outro usuário com esse CPF"})
    ranking_points = models.PositiveIntegerField(default=0)
    general_points = models.PositiveIntegerField(default=0)


class Place(models.Model): # Address
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
    

class Attending(models.Model):
    STATUS_ATTENING_CHOICES = [
        ('CA', 'Confirmado atendimento'),
        ('AG', 'Aguardando confirmação'),
        ('CC', 'Cancelado'),
        ('AD', 'Aguardando confirmação de Doação'),
        ('CD', 'Concluído')
    ]
    requester = ForeignKey(Donnor, on_delete=CASCADE)
    recipient = ForeignKey(RecyclingCenter, on_delete=CASCADE)
    place = models.CharField(max_length=100)
    #address = models.ForeignKey(Address,) instead
    date_attending = models.DateTimeField()
    #date_attending = models.DateField() #instead
    #time_attending = models.TimeField() #instead
    obs = models.TextField(max_length=500)
    status_attending = models.CharField(max_length=2, choices=STATUS_ATTENING_CHOICES)
    #date_modification = models.DateTimeField(null=True, blank=True) 
    #date_joined = models.DateTimeField(auto_now_add=True)

    confirmed = models.BooleanField(default=None, null=True, blank=True)
    return_recipient = models.TextField(max_length=300)
    points_attending = models.TextField(default=0)
    #type_attending = models.CharField(max_length=2) # choices=(Avulso, Marcado)


class Messages(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    attending = models.ForeignKey(Attending, on_delete=CASCADE)
    message = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)


class Donation(models.Model):
    attending = OneToOneField(Attending, on_delete=CASCADE, null=True, blank=True)
    donor_id = models.ForeignKey(Donnor, on_delete=CASCADE)
    recyclingCenter_id = models.ForeignKey(RecyclingCenter, on_delete=CASCADE)
    description = models.TextField(max_length=300, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=None, null=True, blank=True)
    added_points = models.PositiveIntegerField(default=0) # null=True, blank=True


class RecyclabelMaterial(models.Model): # Material
    donation_id = models.ForeignKey(Donation, on_delete=CASCADE)
    material_name = models.CharField(max_length=100, null=False, blank=False)
    quatity = models.PositiveIntegerField(null=False, blank=False)
    #kg = models.DecimalField() # instead
    #points = models.FloatField()
    #type_material = CharField()