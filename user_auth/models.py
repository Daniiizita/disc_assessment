from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from disc.models import ResultadoDISC



#Dicionarios de NIVEIS DE EDUCACAO e GENERO e STATUS EDUCACAO

NIVEL_EDUCACAO_CHOICES = [
    ('fundamental', 'Ensino Fundamental'),
    ('medio', 'Ensino Médio'),
    ('tecnico', 'Ensino Técnico'),
    ('superior', 'Ensino Superior'),
    ('pos_graduacao', 'Pós-graduação'),
    ('mestrado', 'Mestrado'),
    ('doutorado', 'Doutorado'),
]

STATUS_EDUCACAO_CHOICES = [
    ('cursando', 'Cursando'),
    ('concluido', 'Concluído'),
    ('interrompido', 'Incompleto'),
]

GENERO_CHOICES = [
    ('feminino', 'Feminino'),
    ('masculino', 'Masculino'),
    ('nao_binario', 'Não-binário'),
    ('outro', 'Outro'),
    ('prefiro_nao_dizer', 'Prefiro Não Dizer'),
]

class CustomUser(AbstractUser): # Herda de AbstractUser #cadastra usuario
    
    # Chave estrangeira para o resultado do teste DISC
    resultado_disc = models.OneToOneField(ResultadoDISC, on_delete=models.SET_NULL, null=True, blank=True, related_name='user')



    # Campo de relação muitos-para-muitos com o modelo Group
    # related_name='customuser_groups': Define um nome exclusivo para a relação reversa de Group para CustomUser
    # blank=True: Permite que o campo seja deixado em branco
    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    
    
    # Campo de relação muitos-para-muitos com o modelo Permission
    # related_name='customuser_user_permissions': Define um nome exclusivo para a relação reversa de Permission para CustomUser
    # blank=True: Permite que o campo seja deixado em branco
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_user_permissions', blank=True)
    
    
    #campos de cadastro que estendem o AbstractUser
    telefone = models.CharField(max_length=15, null=True, blank=True)
    profissao = models.CharField(max_length=100, null=True, blank=True)
    nivel_educacao = models.CharField(choices=NIVEL_EDUCACAO_CHOICES, max_length=20, null=True, blank=True)
    status_educacao = models.CharField(choices= STATUS_EDUCACAO_CHOICES, max_length=100, null=True, blank=True)
    genero = models.CharField(choices=GENERO_CHOICES, max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    localizacao = models.CharField(max_length=100, null=True, blank=True)
    setor = models.CharField(max_length=100, null=True, blank=True)
    # Outros campos personalizados
    

