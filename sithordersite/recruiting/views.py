from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import *

# Create your views here.


def index(request):
    """View function for home page of site."""
    context = dict()
    return render(request, 'index.html', context)


class RecruitCreate(CreateView):
    model = Recruit
    fields = ['name', 'planet', 'age', 'email']

    def get_success_url(self):
        return reverse('home')          # заменить на страницу с тестом


class SithListView(ListView):
    model = Sith
    paginate_by = 10


class SithDetail(DetailView):
    model = Sith