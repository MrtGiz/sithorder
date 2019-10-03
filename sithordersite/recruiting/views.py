from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse, redirect

from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from django.urls import reverse

from .models import *

from . import forms

# Create your views here.


def index(request):
    """View function for home page of site."""
    context = dict()
    return render(request, 'index.html', context)


class RecruitCreate(CreateView):
    model = Recruit
    fields = ['name', 'planet', 'age', 'email']

    def get_success_url(self):
        return reverse('recruit-testing', kwargs={'pk': self.object.id})          # заменить на страницу с тестом


class SithListView(ListView):
    model = Sith
    paginate_by = 10


class SithDetail(DetailView):
    model = Sith


def save_answer(request, question, answer, test_instance):
    TestAnswers.objects.create(
        to_question=TestQuestions.objects.all().get(pk=question),
        test=test_instance,
        answer=answer,
    ).save()


def recruit_test(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    test_questions = TestQuestions.objects.filter(is_used_in_test=True).order_by('id')

    test = Test.objects.create(recruit=recruit)
    test.questions.set(test_questions)
    form = forms.QuestionsForm(request.POST or None, questions=test_questions)

    if request.method == 'POST':
        print('im here!')
        form = forms.QuestionsForm(request.POST or None, questions=test_questions)
        if form.is_valid():
            for (question, answer) in form.answers():
                save_answer(request, question, answer, test)
            print('im here!')
            return redirect('home')
    else:
        print('im here111')
        return render(request, 'recruiting/recruit_test.html', {'form': form, 'recruit': recruit})

