
from django.db import models


class Experiment(models.Model):
    experiment_code = models.CharField(max_length=5)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return self.experiment_code


class News(models.Model):
    is_fake = models.BooleanField()
    topic = models.CharField(max_length=30)
    doc = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    ver_doc = models.CharField(max_length=200)
    ver_title = models.CharField(max_length=300)

    def __str__(self):
        return self.doc


class User(models.Model):
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    news_fake_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='fake_key')
    news_true_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='true_key')
    first_true = models.BooleanField()
    browser_language = models.CharField(max_length=2)
    user_agent = models.CharField(max_length=20)
    origin = models.CharField(max_length=50)
    date_arrive = models.DateTimeField()
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
    question_code = models.CharField(max_length=5)
    text = models.CharField(max_length=200)
    desc = models.CharField(max_length=100)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_code


class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

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
    value = models.TextField()  #TODO: check whether TextField is the best type!


class ErrorTrack(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=200)
    error_cod = models.CharField(max_length=200)
