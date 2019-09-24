from django.db import models
from sithordersite.settings import charfield_length

# Create your models here.


class Planet(models.Model):
    title = models.CharField(max_length=charfield_length, help_text='Введите наименование планеты')

    def __str__(self):
        return self.title


class Sith(models.Model):
    name = models.CharField(max_length=charfield_length, help_text='Введите имя')
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT, help_text='Планета, на которой вы обучаете')

    def __str__(self):
        return self.name

    # def shadow_hand_count(self):


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
    master = models.ForeignKey('Sith', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

