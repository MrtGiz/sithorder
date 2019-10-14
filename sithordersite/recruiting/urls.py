from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('recruit/create/', views.RecruitCreate.as_view(), name='recruit_create'),
    path('siths/', views.SithListView.as_view(), name='sith-list'),
    path('sith/<int:pk>', views.RecruitListView.as_view(), name='recruit-list'),
    path('recruit/test/<int:pk>', views.recruit_test, name='recruit-testing'),
    path('siths/all/', views.full_sith_list, name='full-sith-list'),
    path('siths/more/', views.more_than_one_list, name='more-than-one'),
]
