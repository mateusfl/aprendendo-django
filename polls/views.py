from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

# Create your views here.
def index(request):
    ultimas_enquetes = Question.objects.order_by("-pub_date")[:5]
    context = {
        "ultimas_enquetes": ultimas_enquetes,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": q})


def results(request, question_id):
    return HttpResponse(f"Você está na página dos resultados da pergunta {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Você está votando na pergunta {question_id}")
