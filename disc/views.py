from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from disc.models import Pergunta, ResultadoDISC
from .forms import QuestionnaireForm
from django.views.generic import DetailView
from django.http import JsonResponse
from django.db.models import Sum


"""def form_valid(self, form):
    # Dicionário para armazenar as pontuações
    pontuacoes = {'d': 0, 'i': 0, 's': 0, 'c': 0}
    contagem = {'d': 0, 'i': 0, 's': 0, 'c': 0}
    
    # Processar as respostas
    for name, value in form.cleaned_data.items():
        pergunta_id = int(name.split('_')[1])
        pergunta = Pergunta.objects.get(pk=pergunta_id)
        pontuacoes[pergunta.perfil] += int(value)
        contagem[pergunta.perfil] += 1"""
    
# Calculando a média
class QuestionnaireView(FormView): #antigo PerguntaView
        form_class = QuestionnaireForm
        template_name = 'teste_disc.html'
        success_url = None

        def form_valid(self, form):
            # Dicionário para armazenar as pontuações
            pontuacoes = {'d': 0, 'i': 0, 's': 0, 'c': 0}
            contagem = {'d': 0, 'i': 0, 's': 0, 'c': 0}

            # Processar as respostas
            for name, value in form.cleaned_data.items():
                pergunta_id = int(name.split('_')[1])
                pergunta = Pergunta.objects.get(pk=pergunta_id)
                pontuacoes[pergunta.perfil] += int(value)
                contagem[pergunta.perfil] += 1

            # Calculando a média
            medias = {perfil: pontuacoes[perfil]/contagem[perfil] for perfil in pontuacoes}

            # Salvar as médias no modelo ResultadoDISC
            resultado = ResultadoDISC(
                dominante=medias['d'],
                influente=medias['i'],
                estabilidade=medias['s'],
                conformado=medias['c']
            )
            resultado.save()

            # Associa o resultado DISC ao usuário se ele estiver logado
            if self.request.user.is_authenticated:
                self.request.user.resultado_disc = resultado
                self.request.user.save()

            # Redireciona para a página de resultados (logado ou anônimo)
            self.success_url = reverse_lazy('disc:resultado', kwargs={'pk': resultado.id})

            return super(QuestionnaireView, self).form_valid(form)


#mostrando o resultado

class ResultadoView(DetailView):
    
    model = ResultadoDISC
    template_name = 'resultado_disc.html'
    
    def get_context_data(self, **kwargs):
        
        PERFIL_MAP = {
        'd': 'Dominante',
        'i': 'Influente',
        's': 'Estabilidade',
        'c': 'Conformado'
    }
        PERFIL_DESCRICAO = {
        'd': 'Perfil Dominante: Indivíduos com características assertivas e orientados para resultados. São diretos, assertivos e orientados para metas, frequentemente assumindo o controle e tomando decisões rapidamente.',
        'i': 'Perfil Influente: Pessoas comunicativas e sociáveis, que gostam de interações sociais. São otimistas, persuasivos e gostam de influenciar os outros. Tendem a ser expressivos e energéticos.',
        's': 'Perfil Estabilidade: Indivíduos estáveis e consistentes, valorizam a harmonia e a segurança. São pacientes, leais e preferem ambientes mais previsíveis. Tendem a ser calmos e amigáveis.',
        'c': 'Perfil Conformado: Pessoas precisas e analíticas, que valorizam a precisão e os detalhes. São cautelosos, meticulosos e buscam a exatidão. Tendem a ser lógicos e focados em procedimentos.'
    }

        LOCAIS_TRABALHO = {
        'd': 'Ambientes onde a liderança assertiva e a tomada de decisão rápida são valorizadas, como cargos de gestão, empreendedorismo ou áreas competitivas como vendas e negociações.',
        'i': 'Trabalhos que envolvam interação social e comunicação, como marketing, relações públicas, áreas de entretenimento, vendas e cargos que exijam networking.',
        's': 'Ambientes com equilíbrio, estabilidade e foco em relações interpessoais, como serviços sociais, áreas de suporte ao cliente, administração e cargos que demandem paciência e cooperação.',
        'c': 'Atividades que valorizem precisão e análise detalhada, como engenharia, desenvolvimento de software, áreas financeiras, pesquisa científica e cargos que demandem rigor técnico e meticulosidade.'
    }

        
        context = super().get_context_data(**kwargs)
        inicial_perfil_mais_alto = self.object.perfil_mais_alto
        context['perfil_mais_alto'] = PERFIL_MAP[inicial_perfil_mais_alto]
        context['descricao_perfil'] = PERFIL_DESCRICAO[inicial_perfil_mais_alto]
        context['locais_trabalho'] = LOCAIS_TRABALHO[inicial_perfil_mais_alto]
    
        return context
    

def estatisticas_disc(request):
    # Buscar todos os resultados dos testes DISC
        # Filtra os resultados do DISC que têm um usuário associado
    resultados = ResultadoDISC.objects.filter(user__isnull=False)
    

    # Inicializar contadores para cada perfil
    contagem_perfis = {'d': 0, 'i': 0, 's': 0, 'c': 0}
    
    # Calcular os totais para cada perfil e o total de usuários
    total_usuarios = resultados.count()
    total_d = resultados.aggregate(Sum('dominante'))['dominante__sum']
    total_i = resultados.aggregate(Sum('influente'))['influente__sum']
    total_s = resultados.aggregate(Sum('estabilidade'))['estabilidade__sum']
    total_c = resultados.aggregate(Sum('conformado'))['conformado__sum']

    data = {
        'total_usuarios': total_usuarios,
        'd': total_d,
        'i': total_i,
        's': total_s,
        'c': total_c
    }
    
    
    # Contar o perfil mais alto de cada resultado
    for resultado in resultados:
        perfil_mais_alto = resultado.perfil_mais_alto
        contagem_perfis[perfil_mais_alto] += 1

    # Criar a resposta JSON com a contagem dos perfis
    resposta = {
        'd': contagem_perfis['d'],
        'i': contagem_perfis['i'],
        's': contagem_perfis['s'],
        'c': contagem_perfis['c']
    }

    return JsonResponse(resposta)

