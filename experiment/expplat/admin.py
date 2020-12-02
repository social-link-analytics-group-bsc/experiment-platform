
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import SimpleListFilter
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from .models import Experiment, News, User, QuestionType, Question, Choice, QuestionExperiment, Answer, ErrorTrack
import csv


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class GenderFilter(MultipleChoiceListFilter):
    title = 'Gender'
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmgen')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmgen')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)

class AgeFilter(MultipleChoiceListFilter):
    title = 'Age'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmage')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmage')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class ProvinceFilter(MultipleChoiceListFilter):
    title = 'Province / location'
    parameter_name = 'province'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmprv')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmprv')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class EducationFilter(MultipleChoiceListFilter):
    title = 'Education level'
    parameter_name = 'education'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmedu')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmedu')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class ProfessionFilter(MultipleChoiceListFilter):
    title = 'Profession'
    parameter_name = 'profession'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmpro')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmpro')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class EmploymentFilter(MultipleChoiceListFilter):
    title = 'Employment status'
    parameter_name = 'employment'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmjob')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmjob')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class ReligionFilter(MultipleChoiceListFilter):
    title = 'Religion'
    parameter_name = 'religion'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmrel')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmrel')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class PoliticalFilter(MultipleChoiceListFilter):
    title = 'Political orientation'
    parameter_name = 'politics'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmpol')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmpol')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class TechFilter(MultipleChoiceListFilter):
    title = 'Technical skills'
    parameter_name = 'tech'

    def lookups(self, request, model_admin):
        que = Question.objects.filter(question_code='dmtec')[0]
        agent_objs = que.choice_set.all()
        agents = []
        for agent_obj in agent_objs:
            agents.append((agent_obj.value, str(agent_obj.value)))
        return tuple(agents)

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value.split(",")
        que = Question.objects.filter(question_code='dmtec')[0]
        ans = Answer.objects.filter(question_id=que.id, value__in=value)
        ids = []
        for an in ans:
            ids.append(an.user_id.id)
        return queryset.filter(id__in=ids)


class FinishFilter(SimpleListFilter):
    title = 'Experiment state'
    parameter_name = 'date_finish'

    def lookups(self, request, model_admin):
        return tuple([(False, "Finished"), (True, "Not finished")])

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        value = value == "True"
        return queryset.filter(date_finish__isnull=value)


class UsersAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id', 'date_start', 'date_finish', 'state']
    list_display += ['fake_news', 'true_news']
    list_display += ['gender', 'age', 'location', 'education', 'profession', 'employment']
    list_display += ['religion', 'politics', 'tech']
    #list_display += ['browser_language', 'user_agent_mobile', 'user_agent_pc', 'user_agent_os', 'user_agent_browser']
    ordering = ('-date_arrive', )
    list_filter = (FinishFilter, GenderFilter, AgeFilter)
    list_filter += (ProvinceFilter, EducationFilter, ProfessionFilter, EmploymentFilter)
    list_filter += (ReligionFilter, PoliticalFilter, TechFilter)
    actions = ["export_as_csv"]

    class Media:
        js = ['js/jquery.js', 'admin/js/list_filter_collapse.js']

    def date_start(self, obj):
        return obj.date_arrive

    def fake_news(self, obj):
        return obj.news_fake_id
    fake_news.short_description = 'Fake News'

    def true_news(self, obj):
        return obj.news_true_id
    true_news.short_description = 'True News'

    def state(self, obj):
        if obj.date_finish is not None:
            return 'Finished'
        else:
            return 'Not finished'

        # if obj.date_finish is not None:
        #     return 'result'
        # elif obj.time_rutina > 0:
        #     return 'rutina'
        # elif obj.time_demo > 0:
        #     return 'demo'
        # elif obj.time_answer > 0:
        #     return 'answer'
        # elif obj.time_news2 > 0:
        #     return 'news 2'
        # elif obj.time_news1 > 0:
        #     return 'news 1'
        # else:
        #     return 'index'

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

    def age(self, obj):
        return self.translateAns('dmage', obj)

    def location(self, obj):
        return self.translateAns('dmprv', obj)

    def education(self, obj):
        return self.translateAns('dmedu', obj)

    def profession(self, obj):
        return self.translateAns('dmpro', obj)    

    def religion(self, obj):
        return self.translateAns('dmrel', obj)

    def politics(self, obj):
        return self.translateAns('dmpol', obj)

    def tech(self, obj):
        return self.translateAns('dmtec', obj)
    tech.short_description = 'Tech Skills'

class AnsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'question_code', 'question_desc', 'value']
    # list_filter = ("user_id", "value")

    def question_code(self, obj):
        return obj.question_id.question_code

    def question_desc(self, obj):
        return obj.question_id.text


class NewsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id', 'title', 'source', 'is_fake']
    list_display += ['appeared', 'appeared2', 'ans_true', 'ans_fake', 'error']
    list_filter = ('is_fake', 'error')
    actions = ["export_as_csv"]

    def appeared(self, obj):
        if obj.is_fake:
            usrs = User.objects.filter(news_fake_id=obj.id)
            return len(usrs)
        else:
            usrs = User.objects.filter(news_true_id=obj.id)
            return len(usrs)
    appeared.short_description = 'Freq'

    def appeared2(self, obj):
        if obj.is_fake:
            usrs = User.objects.filter(news_fake_id=obj.id, date_finish__isnull=False)
            return len(usrs)
        else:
            usrs = User.objects.filter(news_true_id=obj.id, date_finish__isnull=False)
            return len(usrs)
    appeared2.short_description = 'Frequency Finished'

    def ans_true(self, obj):
        if obj.is_fake:
            que = Question.objects.filter(question_code='fysno')[0]
            usrs = User.objects.filter(news_fake_id=obj.id)
            usrs_id = []
            for usr in usrs:
                usrs_id.append(usr.id)
            ans = Answer.objects.filter(user_id__in=usrs_id, question_id=que.id, value='sí')
            return len(ans)
        else:
            que = Question.objects.filter(question_code='tysno')[0]
            usrs = User.objects.filter(news_true_id=obj.id)
            usrs_id = []
            for usr in usrs:
                usrs_id.append(usr.id)
            ans = Answer.objects.filter(user_id__in=usrs_id, question_id=que.id, value='sí')
            return len(ans)
    ans_true.short_description = 'True'

    def ans_fake(self, obj):
        if obj.is_fake:
            que = Question.objects.filter(question_code='fysno')[0]
            usrs = User.objects.filter(news_fake_id=obj.id)
            usrs_id = []
            for usr in usrs:
                usrs_id.append(usr.id)
            ans = Answer.objects.filter(user_id__in=usrs_id, question_id=que.id, value='no')
            return len(ans)
        else:
            que = Question.objects.filter(question_code='tysno')[0]
            usrs = User.objects.filter(news_true_id=obj.id)
            usrs_id = []
            for usr in usrs:
                usrs_id.append(usr.id)
            ans = Answer.objects.filter(user_id__in=usrs_id, question_id=que.id, value='no')
            return len(ans)
    ans_fake.short_description = 'Fake'


admin.site.register(Experiment)
admin.site.register(News, NewsAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionExperiment)
admin.site.register(Answer, AnsAdmin)
admin.site.register(ErrorTrack)
