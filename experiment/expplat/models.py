
from django.db import models
from django.utils import timezone


class Experiment(models.Model):
    experiment_code = models.CharField(max_length=5)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return self.experiment_code


class News(models.Model):
    is_fake = models.BooleanField(null=True)
    topic = models.CharField(max_length=30, default='')
    doc = models.CharField(max_length=200, default='')
    source = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=300, default='')
    ver_doc = models.CharField(max_length=200, default='')
    ver_title = models.CharField(max_length=300, default='')
    error = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(models.Model):
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    news_fake_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='fake_key')
    news_true_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='true_key')
    first_true = models.BooleanField(null=True)
    reread_fake = models.BooleanField(default=False)
    reread_true = models.BooleanField(default=False)
    browser_language = models.CharField(max_length=2, default='')
    user_agent = models.CharField(max_length=200, default='')
    user_agent_mobile = models.BooleanField(null=True)
    user_agent_pc = models.BooleanField(null=True)
    user_agent_browser = models.CharField(max_length=200, default='')
    user_agent_os = models.CharField(max_length=200, default='')
    user_agent_device = models.CharField(max_length=200, default='')
    date_arrive = models.DateTimeField(default=timezone.now)
    date_finish = models.DateTimeField(null=True)
    time_index = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_news1 = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_news2 = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_answer = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_demo = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_rutina = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    time_result = models.DecimalField(max_digits=5, decimal_places=0, default=0)

    def __str__(self):
        return str(self.id)


class QuestionType(models.Model):
    type = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Question(models.Model):
    question_code = models.CharField(max_length=5, default='')
    text = models.CharField(max_length=200, default='')
    desc = models.CharField(max_length=100, default='')
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_code


class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.question_id) + str(self.value)


class QuestionExperiment(models.Model):
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Answer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField(default='')


class ErrorTrack(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=200, default='')
    error_cod = models.CharField(max_length=200, default='')
