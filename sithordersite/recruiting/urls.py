from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('recruit/create/', views.RecruitCreate.as_view(), name='recruit_create'),
    path('siths/', views.SithListView.as_view(), name='sith-list'),
    path('sith/<int:pk>', views.SithDetail.as_view(), name='sith-detail'),
    path('recruit/test/<int:pk>', views.recruit_test, name='recruit-testing'),

]
