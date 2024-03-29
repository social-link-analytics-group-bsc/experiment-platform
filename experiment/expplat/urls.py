
from django.urls import path
from . import views


app_name = 'expplat'
urlpatterns = [
    path('', views.index, name='index'),
    path('read_news_1/', views.read_news_1, name='read_news_1'),
    path('read_news_2/', views.read_news_2, name='read_news_2'),
    path('answer/', views.answer, name='answer'),
    path('result/', views.result, name='result'),
    path('notloadnews/', views.notLoadNews, name='notloadnews'),
    path('rereadnews/', views.rereadNews, name='rereadnews'),
    path('read_all_news_at_once_2020/', views.read_all_news_at_once, name='read_all_news_at_once'),
    path('demuestran_5g_covid', views.demuestran_5g_covid, name='demuestran_5g_covid')
]
