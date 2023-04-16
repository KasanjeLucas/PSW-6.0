from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.messages import constants
import re
# Create your views here.

def register(request):
    
    # Comparando requisições
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # Validação de senha
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, ('As senhas não coincidem'))
            return redirect('/users/register')
        
        # Validação se o usuário digitou algo
        if username == '' and email == '' and senha == '' and confirmar_senha == '':
            messages.add_message(request, constants.WARNING, ('Você não digitou nada. Por favor, tente novamente.'))
            return redirect('/users/register')
        # Validação de força da senha:
        if not (re.search(r'.{8,}', senha) and   
           re.search(r'[A-Z]', senha) and 
           re.search(r'\d', senha)):
            messages.add_message(request, constants.ERROR, ('Sua senha deve ter no mínimo 8 caracteres, uma letra maiúscula, um caractere especial (sem emojis) e um número.'))
            return redirect('/users/register')
        # Tomando uma flag de comparação com usuários existentes
        user = User.objects.filter(email=email)
        
        # Comparando com os usuários já cadastrados
        if user.exists():
            # Caso exista, é redirecionado para a tela de registro
            messages.add_message(request, constants.ERROR, ('Usuário já cadastro em nosso sistema.'))
            return redirect(reverse('register'))
        
        # Caso não exista um usuários igual, um novo é criado sem problemas
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        messages.add_message(request, constants.SUCCESS, ('Usuário cadastrado com sucesso.'))
        return (redirect(reverse('login')))


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(username=username, password=senha)
        
        if not user:
            messages.add_message(request, constants.ERROR, ('Username e/ou senha inválidos.'))
            return redirect(reverse('login'))
        
        auth.login(request, user)
        return redirect(reverse('novo_evento'))

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')