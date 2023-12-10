from django.urls import path

from .views import send_login_email, login, logout

urlpatterns = [
    path('send_login_email', send_login_email, name='send_login_email'),
    path('login', login, name='login'),
    path('logout', logout, name='logout')
]