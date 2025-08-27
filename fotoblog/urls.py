from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
)
from authentication.views import signup
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

    # App
    path('home/', blog.views.home, name='home'),
]
