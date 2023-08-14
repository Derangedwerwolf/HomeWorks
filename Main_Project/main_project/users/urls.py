from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.forms import LoginForm
from users.views import RegisterView

app_name = 'users'

urlpatterns = [
    path("register/", RegisterView.as_view(template_name="register.html"), name="register"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                     authentication_form=LoginForm), name="login"),
    path("logout/", LogoutView.as_view(template_name='logout.html'), name="logout"),
]