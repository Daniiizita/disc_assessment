from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('redirecionar_cadastro/', views.redirecionar_cadastro, name='redirecionar_cadastro'),
]