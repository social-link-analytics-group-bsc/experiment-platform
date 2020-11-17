
from django.urls import path
from . import views


app_name = 'expplat'
urlpatterns = [
    path('', views.index, name='index'),
    path('read_news_1/', views.read_news, name='read_news_1'),
    path('read_news_2/', views.read_news, name='read_news_2'),
    path('answer/', views.answer, name='answer'),
    path('demo/', views.demo, name='demo'),
    path('rutina/', views.rutina, name='rutina'),
    path('result/', views.result, name='result'),
    path('notloadnews/', views.notLoadNews, name='notloadnews')
]
