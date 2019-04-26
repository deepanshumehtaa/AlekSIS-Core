from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Answer(models.Model):
    answer_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = "Antwort"
        verbose_name_plural = "Antworten"

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    answered = models.BooleanField(verbose_name="Beantwortet", default=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"