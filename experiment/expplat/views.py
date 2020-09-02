
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import random as rnd
from .models import Experiment, News, User, QuestionType, Question, Choice, QuestionExperiment, Answer


# Create your views here.
def index(request):

    #TODO: how to choose the experiment? Env variable? Field of active experiment? Solve these deployment issues
    exp = Experiment.objects.all()[0]

    # from all news, one article is taken randomly as the first article to be read
    allnews = News.objects.all()
    first_int = rnd.randint(0, len(allnews)-1)
    first_new = allnews[first_int]

    # if the first article is fake, one from the true news is chosen and othewise if the first article is true
    othernews = News.objects.filter(fake=(not first_new.fake))
    second_int = rnd.randint(0, len(othernews)-1)
    second_new = othernews[second_int]

    # define the true and fake article that will be shown in the experiment
    if first_new.fake:
        fake_new = first_new
        true_new = second_new
    else:
        fake_new = second_new
        true_new = first_new

    # save session keys on the articles to be read and the position in the workflow
    request.session['new1'] = first_new.id
    request.session['new2'] = second_new.id
    request.session['news_fake'] = fake_new.id
    request.session['news_true'] = true_new.id
    request.session['state'] = "index"

    # user instance is initiated and the news and other useful information is saved
    usr = User(
        experiment_id=exp,
        news_fake_id=fake_new, news_true_id=true_new,
        origin='bsc.es', #TODO: get user origin from "request"
        browser_language='ca', #TODO: get browser_language from "request"
        user_agent='firefox', #TODO: get user agent from "request"
        date_arrive=timezone.now()
    )

    # save in session the user_id to identify it in following steps
    usr.save()
    request.session['user_id'] = usr.id

    return render(request, 'expplat/index.html')


def read_news(request):
    if request.session['state'] == 'index':
        target = 'expplat:read_news'
        request.session['state'] = 'news1'
        new = News.objects.filter(id=request.session['new1'])[0]
    elif request.session['state'] == 'news1':
        target = 'expplat:answer'
        request.session['state'] = 'news2'
        new = News.objects.filter(id=request.session['new2'])[0]
    else:
        target = 'expplat:index'
        request.session['state'] = 'index'

    #TODO: prepare other description variables for the template (like title)
    doc = new.doc
    return render(request, 'expplat/read_news.html', {'doc': doc, 'target': target })


def answer(request):
    request.session['state'] = 'answer'

    #TODO: filter only the questions for this experiment
    questions = Question.objects.all()

    #TODO: save time in user
    user_id = request.session['user_id']
    usr = User.objects.filter(id=user_id)[0]

    return render(request, 'expplat/answer.html', { 'questions': questions })


def result(request):
    data = request.POST

    #TODO: filter only the questions for this experiment
    questions = Question.objects.all()
    user_id = request.session['user_id']
    usr = User.objects.filter(id=user_id)[0]
    for que in questions:
        ans = Answer(user_id=usr, question_id=que, value=data[que.question_code])
        ans.save()

    #TODO: get the correct news from session keys or user instance
    news1 = get_object_or_404(News, pk=1)
    news2 = get_object_or_404(News, pk=2)

    return render(request, 'expplat/result.html', { 'news1': news1, 'news2': news2 })
