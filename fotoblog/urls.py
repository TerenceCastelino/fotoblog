from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
)
from authentication.views import signup,upload_profile_photo
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('signup/', signup, name='signup'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('password/change/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'
    ), name='password_change'),

    path('password/change/done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ), name='password_change_done'),

    
    path('home/', blog.views.home, name='home'),

    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),

    path("upload-profile-photo/", upload_profile_photo, name="upload_profile_photo"),

    path('blog/create', blog.views.blog_and_photo_upload, name='blog_create'),

    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),

    path('blog/<int:blog_id>/edit', blog.views.edit_blog, name='edit_blog'),

    path('photo/upload-multiple/', blog.views.create_multiple_photos,
    name='create_multiple_photos'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
