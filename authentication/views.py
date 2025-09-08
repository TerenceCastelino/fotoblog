from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm , UploadProfilePhotoForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", {"form": form})


@login_required  # 🔒 Seuls les utilisateurs connectés peuvent accéder à cette vue
def upload_profile_photo(request):
    if request.method == "POST":
        # 📝 On crée le formulaire avec les données envoyées :
        # - request.POST = champs texte
        # - request.FILES = fichiers uploadés (ici la photo)
        # - instance=request.user = on met à jour l'utilisateur connecté (et non un autre)
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)

        # ✅ On valide le formulaire
        if form.is_valid():
            # 💾 On sauvegarde la nouvelle photo dans le champ profile_photo de l'utilisateur
            form.save()
            # 🔄 On redirige vers la page définie par LOGIN_REDIRECT_URL (ex: /profile/ ou /)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        # 📄 Si GET (ou autre méthode), on prépare un formulaire prérempli avec l'utilisateur actuel
        form = UploadProfilePhotoForm(instance=request.user)

    # 🎨 On affiche le template upload_profile_photo.html en passant le formulaire au contexte
    return render(request, "authentication/upload_profile_photo.html", {"form": form})