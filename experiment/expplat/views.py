
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import time
import random as rnd
from .models import Experiment, News, User, Question, Answer
from django.shortcuts import redirect
from django.urls import reverse


def goIndex():
    return redirect(reverse('expplat:index'))


def saveAnswers(startQue, data, usr):

    startQuestions = Question.objects.filter(question_code__startswith=startQue)

    for que in startQuestions:
        if que.question_code in data.keys():
            ans = Answer(user_id=usr, question_id=que, value=data[que.question_code])
            ans.save()
        else:
            value = '-'
            if que.type == 'radio':
                value = 'unchecked'
            elif que.type == 'input':
                value = data[que.question_code]
            ans = Answer(user_id=usr, question_id=que, value=value)
            ans.save()


def saveTimes(request, current):
    usr = User.objects.filter(id=request.session['user_id'])[0]
    last_state = request.session['state']
    fieldTime = 'time_' + last_state
    fieldDate = 'date_' + last_state
    fieldCurr = 'date_' + current
    request.session[fieldCurr] = int(time.time())

    timeSpent = request.session[fieldCurr] - request.session[fieldDate]

    setattr(usr, fieldTime, getattr(usr, fieldTime) + timeSpent)
    usr.save()


def index(request):

    if 'state' in request.session.keys():
        request.session.flush()

    #TODO: how to choose the experiment? Env variable? Field of active experiment? Solve these deployment issues
    exp = Experiment.objects.all()[0]

    # from all news, one article is taken randomly as the first article to be read
    allnews = News.objects.all()
    first_int = rnd.randint(0, len(allnews)-1)
    first_new = allnews[first_int]

    # if the first article is fake, one from the true news is chosen and othewise if the first article is true
    othernews = News.objects.filter(is_fake=(not first_new.is_fake))
    second_int = rnd.randint(0, len(othernews)-1)
    second_new = othernews[second_int]

    # define the true and fake article that will be shown in the experiment
    if first_new.is_fake:
        first_fake = True
        first_true = False
        fake_new = first_new
        true_new = second_new
    else:
        first_fake = False
        first_true = True
        fake_new = second_new
        true_new = first_new

    # save session keys on the articles to be read and the position in the workflow
    request.session['new1'] = first_new.id
    request.session['new2'] = second_new.id
    request.session['news_fake'] = fake_new.id
    request.session['news_true'] = true_new.id
    request.session['first_fake'] = first_fake
    request.session['state'] = "index"
    request.session['experiment'] = exp.experiment_code
    request.session['date_index'] = int(time.time())

    # user instance is initiated and the news and other useful information is saved
    usr = User(
        experiment_id=exp,
        news_fake_id=fake_new, news_true_id=true_new, first_true=first_true,
        origin='bsc.es', #TODO: get user origin from "request"
        browser_language='ca', #TODO: get browser_language from "request"
        user_agent='firefox', #TODO: get user agent from "request"
        date_arrive=timezone.now(),
        time_index=0,
        time_news1=0,
        time_news2=0,
        time_answer=0,
        time_demo=0,
        time_rutina=0,
        time_result=0
    )

    # save in session the user_id to identify it in following steps
    usr.save()
    request.session['user_id'] = usr.id

    return render(request, 'expplat/index.html')


def read_news(request):

    if 'state' not in request.session.keys():
        return goIndex()

    if request.session['state'] in ['index', 'news2']:
        target = 'expplat:read_news_2'
        moreread = 'block'
        moreans = 'none'
        progress = 25
        saveTimes(request, 'news1')
        request.session['state'] = 'news1'
        new = News.objects.filter(id=request.session['new1'])[0]
    elif request.session['state'] in ['news1', 'answer']:
        target = 'expplat:answer'
        moreread = 'none'
        moreans = 'block'
        progress = 50
        saveTimes(request, 'news2')
        request.session['state'] = 'news2'
        new = News.objects.filter(id=request.session['new2'])[0]
    else:
        return goIndex()


    #TODO: prepare other description variables for the template (like title)
    doc = new.doc
    article = "expplat/notis/" + doc
    return render(request, 'expplat/read_news.html', {'doc': doc, 'target': target, 'moreread': moreread, 'moreans': moreans, 'progress': progress, 'article': article })


def answer(request):

    viewState = 'answer'

    if 'state' not in request.session.keys():
        return goIndex()

    saveTimes(request, viewState)
    request.session['state'] = viewState

    fysno = Question.objects.filter(question_code='fysno')[0]
    fysx = Question.objects.filter(question_code__startswith="fys").exclude(question_code='fysno')
    fnox = Question.objects.filter(question_code__startswith="fno")
    fafx = Question.objects.filter(question_code__startswith="faf")

    tysno = Question.objects.filter(question_code='tysno')[0]
    tysx = Question.objects.filter(question_code__startswith="tys").exclude(question_code='tysno')
    tnox = Question.objects.filter(question_code__startswith="tno")
    tafx = Question.objects.filter(question_code__startswith="taf")

    if request.session['first_fake']:
        quest1 = fysno
        quest1ys = fysx
        quest1no = fnox
        quest1af = fafx
        quest2 = tysno
        quest2ys = tysx
        quest2no = tnox
        quest2af = tafx
    else:
        quest1 = tysno
        quest1ys = tysx
        quest1no = tnox
        quest1af = tafx
        quest2 = fysno
        quest2ys = fysx
        quest2no = fnox
        quest2af = fafx

    news1 = get_object_or_404(News, pk=request.session['new1'])
    news2 = get_object_or_404(News, pk=request.session['new2'])

    return render(request, 'expplat/answer.html', {
        'quest1': quest1, 'quest1ys': quest1ys, 'quest1no': quest1no, 'quest1af': quest1af,
        'quest2': quest2, 'quest2ys': quest2ys, 'quest2no': quest2no, 'quest2af': quest2af,
        'news1': news1, 'news2': news2, 'progress': 75
    })


def demo(request):

    viewState = 'demo'

    if 'state' not in request.session.keys():
        return goIndex()

    saveTimes(request, viewState)
    request.session['state'] = viewState

    if len(request.POST.keys()) == 0:
        print('here without post')
    else:
        data = request.POST

        exp = request.session['experiment']
        user_id = request.session['user_id']
        usr = User.objects.filter(id=user_id)[0]

        fysno = Question.objects.filter(question_code='fysno')[0]
        ans = Answer(user_id=usr, question_id=fysno, value=data['fysno'])
        ans.save()

        fysx = Question.objects.filter(question_code__startswith="fys").exclude(question_code='fysno')
        fnox = Question.objects.filter(question_code__startswith="fno")
        if data['fysno'] == 'si':
            for que in fysx:
                if que.question_code in data.keys():
                    ans = Answer(user_id=usr, question_id=que, value='checked')
                    ans.save()
                else:
                    ans = Answer(user_id=usr, question_id=que, value='unchecked')
                    ans.save()
            for que in fnox:
                ans = Answer(user_id=usr, question_id=que, value='undisplayed')
                ans.save()
        else:
            for que in fysx:
                ans = Answer(user_id=usr, question_id=que, value='undisplayed')
                ans.save()
            for que in fnox:
                if que.question_code in data.keys():
                    ans = Answer(user_id=usr, question_id=que, value='checked')
                    ans.save()
                else:
                    ans = Answer(user_id=usr, question_id=que, value='unchecked')
                    ans.save()

        tysno = Question.objects.filter(question_code='tysno')[0]
        ans = Answer(user_id=usr, question_id=tysno, value=data['tysno'])
        ans.save()

        tysx = Question.objects.filter(question_code__startswith="tys").exclude(question_code='tysno')
        tnox = Question.objects.filter(question_code__startswith="tno")
        if data['tysno'] == 'si':
            for que in tysx:
                if que.question_code in data.keys():
                    ans = Answer(user_id=usr, question_id=que, value='checked')
                    ans.save()
                else:
                    ans = Answer(user_id=usr, question_id=que, value='unchecked')
                    ans.save()
            for que in tnox:
                ans = Answer(user_id=usr, question_id=que, value='undisplayed')
                ans.save()
        else:
            for que in tysx:
                ans = Answer(user_id=usr, question_id=que, value='undisplayed')
                ans.save()
            for que in tnox:
                if que.question_code in data.keys():
                    ans = Answer(user_id=usr, question_id=que, value='checked')
                    ans.save()
                else:
                    ans = Answer(user_id=usr, question_id=que, value='unchecked')
                    ans.save()

    dem = Question.objects.filter(question_code__startswith="dm")

    return render(request, 'expplat/demo.html', {
        'questions': dem, 'progress': 85
    })


def rutina(request):

    viewState = 'rutina'

    if 'state' not in request.session.keys():
        return goIndex()

    saveTimes(request, viewState)
    request.session['state'] = viewState

    if len(request.POST.keys()) == 0:
        print('here without post')
    else:
        data = request.POST

        exp = request.session['experiment']
        user_id = request.session['user_id']
        usr = User.objects.filter(id=user_id)[0]

        saveAnswers("dm", data, usr)

    rut = Question.objects.filter(question_code__startswith="rut")

    return render(request, 'expplat/rutina.html', {
        'questions': rut, 'first': rut[0], 'progress': 95
    })


def result(request):

    viewState = 'result'

    if 'state' not in request.session.keys():
        return goIndex()

    saveTimes(request, viewState)
    request.session['state'] = viewState

    if len(request.POST.keys()) == 0:
        print('here without post')
    else:
        data = request.POST

        user_id = request.session['user_id']
        usr = User.objects.filter(id=user_id)[0]

        saveAnswers("rut", data, usr)


    #TODO: get the correct news from session keys or user instance
    news1 = get_object_or_404(News, pk=request.session['new1'])
    if news1.is_fake:
        news1.display_fake = 'block'
        news1.display_true = 'none'
    else:
        news1.display_fake = 'none'
        news1.display_true = 'block'

    news2 = get_object_or_404(News, pk=request.session['new2'])
    if news2.is_fake:
        news2.display_fake = 'block'
        news2.display_true = 'none'
    else:
        news2.display_fake = 'none'
        news2.display_true = 'block'

    return render(request, 'expplat/result.html', { 'news1': news1, 'news2': news2 })
