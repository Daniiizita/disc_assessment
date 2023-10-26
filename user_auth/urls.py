from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('cadastro/', views.register, name='cadastro'),
    path('login/', views.user_login, name='login'),
    path('perfil/', views.perfil, name='perfil'),  # certifique-se que esta linha exista

    # ... suas outras URLs
]
