from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import Attending, Profile

# Register your models here.
admin.site.register(Profile, auth_admin.UserAdmin)
