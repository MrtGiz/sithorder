from django.db import models
from django.urls import reverse

import uuid

charfield_length = 50


class Planet(models.Model):
    title = models.CharField(max_length=charfield_length, help_text='Введите наименование планеты')

    def __str__(self):
        return self.title


class Sith(models.Model):
    name = models.CharField(max_length=charfield_length, help_text='Введите имя')
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT, help_text='Планета, на которой вы обучаете')

    def __str__(self):
        return self.name

    # функция отображения количества рук тени у ситха
    @property
    def shadow_hand_count(self):
        count_sh = Recruit.objects.filter(master=self).count()
        return count_sh

    def get_absolute_url(self):
        return reverse('sith-detail', args=[str(self.id)])


class Recruit(models.Model):
    name = models.CharField(max_length=charfield_length, help_text='Введите имя')
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT, help_text='Планета, на которой вы обитаете')
    age = models.IntegerField()
    email = models.EmailField(
        unique=True,
        help_text='Введите email',
        max_length=50,
        error_messages={
            'unique': "Данный E-Mail уже зарегистрирован."
        })
    shadow_hand_rank = models.BooleanField(default=False, verbose_name="Наличие звания Руки Тени")
    master = models.ForeignKey('Sith', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_questions_answers(self):
        test = Test.objects.get(recruit=self)
        questions = TestQuestions.objects.filter(is_used_in_test=True)
        question_answer = list()

        for question in questions:
            test_answer = TestAnswers.objects.get(test=test, to_question=question)
            question_answer.append((question, test_answer))
        return question_answer


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный код испытания")
    questions = models.ManyToManyField('TestQuestions', help_text='вопросы в тесте', blank=True)
    recruit = models.ForeignKey('Recruit', on_delete=models.CASCADE, help_text='Рекрут, прошедший данный тест')

    def __str__(self):
        return 'Test CODE: {0}\nRecruit name: {1}'.format(self.id, self.recruit)


class TestQuestions(models.Model):
    question = models.TextField(max_length=300, help_text='Введите текст вопроса')
    is_used_in_test = models.BooleanField(blank=True, default=False,
                                          help_text='Отметьте, чтобы использовать вопрос в тестах',
                                          verbose_name='Использовать в тестах',
                                          )

    def __str__(self):
        return '{0}'.format(self.question)


class TestAnswers(models.Model):
    answer = models.BooleanField()
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    to_question = models.ForeignKey('TestQuestions', on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.answer)
