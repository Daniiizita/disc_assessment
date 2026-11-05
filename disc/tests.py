from django.test import TestCase
from django.urls import reverse

from .models import Pergunta, ResultadoDISC


class QuestionnaireTests(TestCase):
    def setUp(self):
        for perfil in 'discs'[:4]:
            for i in range(2):
                Pergunta.objects.create(texto=f'{perfil}{i}', perfil=perfil)

    def _answers(self, value):
        return {f'pergunta_{p.id}': value for p in Pergunta.objects.all()}

    def test_anonymous_submission_redirects_to_result(self):
        response = self.client.post(reverse('disc:teste_disc'), self._answers(5))
        resultado = ResultadoDISC.objects.get()
        self.assertRedirects(response, reverse('disc:resultado', kwargs={'pk': resultado.id}))

    def test_scores_are_averaged_per_profile(self):
        self.client.post(reverse('disc:teste_disc'), self._answers(4))
        resultado = ResultadoDISC.objects.get()
        self.assertEqual(resultado.dominante, 4)
        self.assertEqual(resultado.conformado, 4)

    def test_result_page_renders(self):
        resultado = ResultadoDISC.objects.create(dominante=5, influente=1, estabilidade=1, conformado=1)
        response = self.client.get(reverse('disc:resultado', kwargs={'pk': resultado.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['perfil_mais_alto'], 'Dominante')
