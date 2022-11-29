from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CrearUsuarioForm, ModificarUsuarioForm
from .models import Usuario

# Register your models here.

class UsuarioAdmin(UserAdmin):
    add_form = CrearUsuarioForm
    form = ModificarUsuarioForm
    model = Usuario
    list_display = ['username', 'telefono', 'puesto', 'organizacion', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + ((None, {"fields":("telefono","puesto", 'organizacion',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields":("telefono","puesto", 'organizacion',)}),)

admin.site.register(Usuario, UsuarioAdmin)