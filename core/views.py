from django.shortcuts import render, redirect
from django.urls import reverse_lazy

def index(request):
    return render(request, 'index.html') 
# Create your views here.

#renderizar a pagina sobre e contato
def sobre(request):
    return render(request, 'sobre.html')

def contato(request):
    return render(request, 'contato.html')

"""
def redirecionar_cadastro(request):
    return redirect(reverse_lazy('user_auth:cadastro'))  # Note o uso de 'user_auth:cadastro'
"""    
