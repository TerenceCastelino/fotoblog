from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )
    # ✅ stocke les avatars dans media/avatars/ et permet de laisser vide
    profile_photo = models.ImageField(
        verbose_name='Photo de profil',
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
