from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # ton modèle personnalisé
        fields = ('username', 'email', 'first_name', 'last_name', 'role')  # ajoute les champs que tu veux exposer
