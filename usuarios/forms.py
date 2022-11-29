from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model= Usuario
        fields = UserCreationForm.Meta.fields + ('telefono', 'puesto','organizacion')

class ModificarUsuarioForm(UserChangeForm):
    class Meta:
        model= Usuario
        fields = UserChangeForm.Meta.fields
        