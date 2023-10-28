from django.shortcuts import render, redirect
from django.contrib.auth import logout
#from django.contrib.auth import authenticate, login
#from .forms import CustomUserForm
#from django.http import HttpResponse
#from disc.models import ResultadoDISC


app_name = 'user_auth'


"""
def register(request): # View para o cadastro de usuários
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('core:index')  # Substituir pelo nome da view para onde redirecionar após o cadastro
    else:
        form = CustomUserForm() # Se não for POST, exibe o formulário para o usuário preencher

    return render(request, 'cadastro.html', {'form': form})
"""
#acima a versão antiga de autenticação sem o allauth

"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_auth:perfil')
        else:
            return HttpResponse('Credenciais inválidas')
    else:
        return render(request, 'login.html')
    
"""
#acima login sem a versão allauth


# user_auth/views.py
def perfil(request):
    resultado_disc = request.user.resultado_disc # Substituir 'usuario' pelo campo que liga o ResultadoDISC ao User
    context = {'resultado_disc': resultado_disc}
    return render(request, 'perfil.html', context)

def user_logout(request):
    logout(request)
    return redirect('core:index')



