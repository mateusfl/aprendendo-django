from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "ultimas_enquetes"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=datetime.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        question_selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Você não selecionou uma opção.",
            },
        )
    else:
        question_selected_choice.votes += 1
        question_selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
