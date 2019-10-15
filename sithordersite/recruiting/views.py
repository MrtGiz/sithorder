from django.shortcuts import render, get_object_or_404, HttpResponse, redirect

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from django.views import View
from django.views.generic.edit import CreateView

from .models import *
from . import forms


def index(request):
    """View function for home page of site."""
    context = dict()
    return render(request, 'index.html', context)


class RecruitCreate(CreateView):
    model = Recruit
    fields = ['name', 'planet', 'age', 'email']

    def get_success_url(self):
        return reverse('recruit-testing', kwargs={'pk': self.object.id})


# class SithListView(ListView):
#     model = Sith
#     paginate_by = 10


def sith_menu(request):
    sith_list = Sith.objects.all()

    if request.method == 'POST':
        # print('POST - sith.id - ', request.POST['sith_id'])
        try:
            sith_id = int(request.POST['sith_id'])
        except (KeyError, Sith.DoesNotExist):
            return redirect('sith-list')
        print('sith_id = ', sith_id)
        print(type(sith_id))
        return redirect('recruit-list', pk=sith_id)

    context = {
        'sith_list': sith_list
    }
    return render(request, 'recruiting/sith_menu.html', context=context)


# class SithDetail(DetailView):
#     model = Sith


def save_answer(request, question, answer, test_instance):
    TestAnswers.objects.create(
        to_question=TestQuestions.objects.all().get(pk=question),
        test=test_instance,
        answer=answer,
    ).save()


def recruit_test(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    test_questions = TestQuestions.objects.filter(is_used_in_test=True).order_by('id')

    # test = Test.objects.create(recruit=recruit)
    # test.questions.set(test_questions)
    form = forms.QuestionsForm(request.POST or None, questions=test_questions)

    if request.method == 'POST':
        print('im here! - test create')
        test = Test.objects.create(recruit=recruit)
        test.questions.set(test_questions)
        form = forms.QuestionsForm(request.POST or None, questions=test_questions)
        if form.is_valid():
            for (question, answer) in form.answers():
                save_answer(request, question, answer, test)
            print('im here! - test saved')
            return redirect('home')
    else:
        print('im here111 - GET')
        context = {
            'form': form,
            'recruit': recruit
        }
        return render(request, 'recruiting/recruit_test.html', context=context)


class RecruitListView(View):
    """
    Вывод списка рекрутов на планете ситха (с его данными и ответами на тестовые вопросы)
    с возможностью зачислить его Рукой Тени
    """
    @staticmethod
    def send_email(recruit):

        subject = 'Зачисление в Орден Ситхов'
        message = 'Добрый день, {0}!\nПоздравляем! Вас приняли в Орден Ситхов! Вашим учителем будет {1}.' \
                  '\nВскоре мы свяжемся с вами для дальнейшего инструктажа.'.format(recruit.name, recruit.master)
        from_email = settings.EMAIL_HOST_USER

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [recruit.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

    def get(self, request, **kwargs):
        print('im here111qwe')
        pk = kwargs.pop('pk')
        sith_instance = get_object_or_404(Sith, pk=pk)
        hands_count = sith_instance.shadow_hand_count

        if hands_count >= 3:
            print('hands count = ', hands_count)
            return render(request, 'recruiting/max_shadow_hands.html')

        planet = sith_instance.planet
        recruits = Recruit.objects.filter(planet=planet, shadow_hand_rank=False).order_by('id')

        context = {
            'sith_instance': sith_instance,
            'hands_count': hands_count,
            'recruits': recruits,
        }
        return render(request, 'recruiting/recruit_list.html', context=context)

    def post(self, request, **kwargs):
        pk = kwargs.pop('pk')

        # if hands_count >= 3:
        #     print('hands count = ', hands_count)
        #     return render(request, 'recruiting/max_shadow_hands.html')
        try:
            recruit = Recruit.objects.get(name=request.POST['recruit'])
        except (KeyError, Recruit.DoesNotExist):
            return redirect('recruit-list', pk=pk)

        sith = Sith.objects.get(pk=pk)
        recruits = Recruit.objects.filter(planet=sith.planet, shadow_hand_rank=False).order_by('id')
        recruit.master = sith
        recruit.shadow_hand_rank = True
        recruit.save()
        self.send_email(recruit)
        print('send email')
        hands_count = sith.shadow_hand_count

        if hands_count >= 3:
            print('hands count = ', hands_count)
            return render(request, 'recruiting/max_shadow_hands.html')

        context = {
            'sith_instance': sith,
            'hands_count': hands_count,
            'recruits': recruits,
        }
        return render(request, 'recruiting/recruit_list.html', context=context)


def full_sith_list(request):
    sith_list = Sith.objects.all()
    context = {
        'sith_list': sith_list
    }
    return render(request, 'recruiting/full_sith_list.html', context=context)


def more_than_one_list(request):
    sith_list = Sith.objects.all()
    new_list = list()
    for sith in sith_list:
        if sith.shadow_hand_count > 1:
            new_list.append(sith)
    context = {
        'sith_list': new_list
    }
    return render(request, 'recruiting/full_sith_list.html', context=context)
