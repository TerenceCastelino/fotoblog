from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class StartsWithUppercaseValidator:
    """
    Validateur personnalisé : oblige les mots de passe
    à commencer par une lettre majuscule.
    """

    def validate(self, password, user=None):
        """
        Méthode principale appelée par Django.
        - password : le mot de passe soumis par l'utilisateur
        - user : l'utilisateur en cours (optionnel, rarement utilisé ici)
        """

        if not password:
            raise ValidationError(
                _("Le mot de passe ne peut pas être vide."),
                code="password_empty",
            )

        # Vérifie que le premier caractère du mot de passe est une majuscule
        if not password[0].isupper():
            raise ValidationError(
                _("Le mot de passe doit commencer par une majuscule."),
                code="password_no_upper_start",
            )

    def get_help_text(self):
        """
        Méthode appelée par Django pour afficher une aide
        sous le champ du formulaire "mot de passe".
        Exemple : dans le formulaire d'inscription, l'utilisateur verra ce message.
        """
        return _("Votre mot de passe doit commencer par une majuscule.")
