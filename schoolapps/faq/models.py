from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FAQQuestion(models.Model):
    question_text = models.TextField()
    icon = models.CharField(max_length=20, blank=True, default="question_answer")

    show = models.BooleanField(verbose_name="Veröffentlicht", default=False)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "FAQ-Frage"
        verbose_name_plural = "FAQ-Fragen"

class Question(models.Model):
    question_text = models.TextField()
    pub_date = models.DateTimeField('date published')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    answered = models.BooleanField(verbose_name="Beantwortet", default=False)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"