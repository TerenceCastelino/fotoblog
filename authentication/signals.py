# authentication/signals.py
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver

from blog.models import Blog, Photo

# On aligne groupes == codes rôle pour éviter tout écart ("CREATOR", "SUBSCRIBER")
MANAGED_GROUPS = {"CREATOR", "SUBSCRIBER"}

def ensure_groups_and_perms():
    # Groupes
    creator_grp, _ = Group.objects.get_or_create(name="CREATOR")
    subscriber_grp, _ = Group.objects.get_or_create(name="SUBSCRIBER")

    # Permissions auto des modèles Blog/Photo
    blog_ct = ContentType.objects.get_for_model(Blog)
    photo_ct = ContentType.objects.get_for_model(Photo)

    add_blog    = Permission.objects.get(codename="add_blog",    content_type=blog_ct)
    change_blog = Permission.objects.get(codename="change_blog", content_type=blog_ct)
    delete_blog = Permission.objects.get(codename="delete_blog", content_type=blog_ct)
    view_blog   = Permission.objects.get(codename="view_blog",   content_type=blog_ct)

    add_photo    = Permission.objects.get(codename="add_photo",    content_type=photo_ct)
    change_photo = Permission.objects.get(codename="change_photo", content_type=photo_ct)
    delete_photo = Permission.objects.get(codename="delete_photo", content_type=photo_ct)
    view_photo   = Permission.objects.get(codename="view_photo",   content_type=photo_ct)

    # SUBSCRIBER : lecture seulement
    subscriber_grp.permissions.set({view_blog, view_photo})

    # CREATOR : tout sur Blog & Photo (à minima add + view ; ici on donne full CRUD)
    creator_grp.permissions.set({
        view_blog, add_blog, change_blog, delete_blog,
        view_photo, add_photo, change_photo, delete_photo,
    })

@receiver(post_migrate)
def sync_groups_after_migrate(sender, **kwargs):
    # Garantit que les groupes/perms existent après chaque migration
    try:
        ensure_groups_and_perms()
    except Exception:
        # Évite de bloquer les migrations si ContentType pas prêt lors d’apps non installées, etc.
        pass

@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def remember_old_role(sender, instance, **kwargs):
    # Pour détecter un changement de rôle
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._old_role = getattr(old, "role", None)
        except sender.DoesNotExist:
            instance._old_role = None
    else:
        instance._old_role = None

def _sync_user_group_for_role(user):
    role = getattr(user, "role", None)
    if not role:
        return
    # Retire des groupes gérés puis ajoute le groupe du rôle courant
    user.groups.remove(*Group.objects.filter(name__in=MANAGED_GROUPS))
    grp, _ = Group.objects.get_or_create(name=role)
    user.groups.add(grp)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_group_on_create_or_role_change(sender, instance, created, **kwargs):
    # S'assure que les groupes existent (utile au premier run)
    try:
        ensure_groups_and_perms()
    except Exception:
        pass
    if created or getattr(instance, "_old_role", None) != getattr(instance, "role", None):
        _sync_user_group_for_role(instance)
