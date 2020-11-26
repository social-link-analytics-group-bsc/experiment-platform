
from django.contrib import admin
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from .models import Experiment, News, User, QuestionType, Question, Choice, QuestionExperiment, Answer, ErrorTrack


class LangFilter(MultipleChoiceListFilter):
    title = 'Lang'
    parameter_name = 'browser_language__in'

    def lookups(self, request, model_admin):
        lang_objs = User.objects.values('browser_language').distinct().order_by('browser_language')
        langs = []
        for lang_obj in lang_objs:
            langs.append((lang_obj['browser_language'], str(lang_obj['browser_language'])))
        return tuple(langs)


class AgentFilter(MultipleChoiceListFilter):
    title = 'AgentBrow'
    parameter_name = 'user_agent_browser__in'

    def lookups(self, request, model_admin):
        agent_objs = User.objects.values('user_agent_browser').distinct().order_by('user_agent_browser')
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj['user_agent_browser'], str(agent_obj['user_agent_browser'])))
        return tuple(agents)


class FinishFilter(MultipleChoiceListFilter):
    title = 'Finished'
    parameter_name = 'date_finish__isnull'

    def lookups(self, request, model_admin):
        return tuple([(False, "Finished"), (True, "Not finished")])





class UsersAdmin(admin.ModelAdmin):
    list_display = ['experiment_id', 'id']
    list_display += ['date_arrive', 'state', 'date_finish']
    list_display += ['fake_news', 'true_news']
    list_display += ['employment', 'gender', 'edad', 'prov', 'educ', 'prof', 'empleo', 'relig', 'polit', 'techie']
    list_display += ['browser_language', 'user_agent_mobile', 'user_agent_pc', 'user_agent_os', 'user_agent_browser']
    list_filter = (FinishFilter, LangFilter, AgentFilter, "experiment_id")


    def fake_news(self, obj):
        return obj.news_fake_id
    fake_news.short_description = 'Fake News'

    def true_news(self, obj):
        return obj.news_true_id
    true_news.short_description = 'True News'

    def state(self, obj):
        ans = len(Answer.objects.filter(user_id=obj.id))
        if ans == 0:
            return 'read'
        elif ans < 40:
            return 'answer'
        elif ans < 50:
            return 'demo'
        elif ans < 60:
            return 'rutina'
        elif ans > 70:
            return 'finish'


    def translateAns(self, code, obj):
        que = Question.objects.filter(question_code=code)[0]
        ans = Answer.objects.filter(user_id=obj.id, question_id=que.id)
        if len(ans) == 0:
            return "-"
        else:
            return ans[0].value

    def employment(self, obj):
        return self.translateAns('dmjob', obj)

    def gender(self, obj):
        return self.translateAns('dmgen', obj)

    def edad(self, obj):
        return self.translateAns('dmage', obj)

    def prov(self, obj):
        return self.translateAns('dmprv', obj)

    def educ(self, obj):
        return self.translateAns('dmedu', obj)

    def prof(self, obj):
        return self.translateAns('dmpro', obj)

    def empleo(self, obj):
        return self.translateAns('dmjob', obj)

    def relig(self, obj):
        return self.translateAns('dmrel', obj)

    def polit(self, obj):
        return self.translateAns('dmpol', obj)

    def techie(self, obj):
        return self.translateAns('dmtec', obj)


class AnsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'question_code', 'question_desc', 'value']
    # list_filter = ("user_id", "value")

    def question_code(self, obj):
        return obj.question_id.question_code

    def question_desc(self, obj):
        return obj.question_id.text


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_fake', 'error', 'topic', 'title']
    list_filter = ('is_fake', 'error')

admin.site.register(Experiment)
admin.site.register(News, NewsAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionExperiment)
admin.site.register(Answer, AnsAdmin)
admin.site.register(ErrorTrack)
