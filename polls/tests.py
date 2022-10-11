import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.
class QuestionModelsTests(TestCase):
    def test_publicado_recentemente_com_data_futura(self):
        """
        was_published_recently() retorna False para datas de criação no futuro
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_publicado_recentemente_com_data_antiga(self):
        """
        was_published_recently() retorna False se a data for antiga
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_publicado_recentemente_com_data_recente(self):
        """
        was_published_recently() retorna True se a data for recente
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def criar_enquete(question_text, days):
    """
    Cria uma enquete com o texto informado
    e 'days' de distância de agora.
    'days' positivos para datas futuras ou negativos
    para datas no passado.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_sem_enquetes(self):
        """
        Mostrar uma mensagem se não houverem enquetes.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhuma enquete disponível.")
        self.assertQuerysetEqual(response.context["ultimas_enquetes"], [])

    def test_enquetes_passadas(self):
        """
        Enquetes com data passada devem estar contidas na lista
        """
        question = criar_enquete(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["ultimas_enquetes"],
            [question],
        )

    def test_enquetes_futuras(self):
        """
        Enquetes com datas futuras não devem estar contidas na lista
        """
        criar_enquete(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Nenhuma enquete disponível.")
        self.assertQuerysetEqual(response.context["ultimas_enquetes"], [])

    def test_enquetes_futuras_e_passadas(self):
        """
        Mesmo que hajam enquetes passadas e futuras, apenas as
        passadas devem ser exibidas.
        """
        question = criar_enquete(question_text="Past question.", days=-30)
        criar_enquete(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["ultimas_enquetes"],
            [question],
        )

    def test_duas_enquetes_passadas(self):
        """
        A página deve poder exibir mais de uma enquete com data passada
        """
        question1 = criar_enquete(question_text="Past question 1.", days=-30)
        question2 = criar_enquete(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["ultimas_enquetes"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_enquete_futura(self):
        """
        A página de detalhes de uma enquete cuja data é futura
        deve retornar uma página de 404.
        """
        future_question = criar_enquete(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_enquete_passada(self):
        """
        Uma página de detalhes de uma enquete com data passada
        deve apresentar o texto da enquete.
        """
        past_question = criar_enquete(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
