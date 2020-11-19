
from django.contrib import admin
from .models import Experiment, News, User, QuestionType, Question, Choice, QuestionExperiment, Answer, ErrorTrack


class UsersAdmin(admin.ModelAdmin):
    list_display = ['experiment_id', 'id', 'browser_language', 'date_arrive', 'ans_count']
    list_filter = ("experiment_id", "browser_language")

    def ans_count(self, obj):
        ans = Answer.objects.filter(user_id=obj.id)
        return len(ans)


class AnsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'question_code', 'question_desc', 'value']
    # list_filter = ("user_id", "value")

    def question_code(self, obj):
        return obj.question_id.question_code

    def question_desc(self, obj):
        return obj.question_id.text


admin.site.register(Experiment)
admin.site.register(News)
admin.site.register(User, UsersAdmin)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionExperiment)
admin.site.register(Answer, AnsAdmin)
admin.site.register(ErrorTrack)
