
from django.contrib import admin
from .models import Experiment, News, User, QuestionType, Question, Choice, QuestionExperiment, Answer

admin.site.register(Experiment)
admin.site.register(News)
admin.site.register(User)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionExperiment)
admin.site.register(Answer)
