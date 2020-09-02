
from django.urls import path
from . import views


app_name = 'expplat'
urlpatterns = [
    path('', views.index, name='index'),
    path('read_news/', views.read_news, name='read_news'),
    path('answer/', views.answer, name='answer'),
    path('result/', views.result, name='result'),
]
