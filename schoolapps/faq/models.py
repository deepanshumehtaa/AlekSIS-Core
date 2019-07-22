from django.db import models
from django.contrib.auth.models import User
from .model_helper import COLORS, ICONS

# Create your models here.
class FAQSection(models.Model):
    name = models.CharField(max_length=200)

    icon = models.CharField(max_length=20, blank=True, default="question_answer", choices=ICONS)
    icon_color = models.CharField(max_length=10, default="black", choices=COLORS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "FAQ-Abschnitt"
        verbose_name_plural = "FAQ-Abschnitte"

class FAQQuestion(models.Model):
    question_text = models.TextField()
    icon = models.CharField(max_length=20, blank=True, default="question_answer", choices=ICONS)

    show = models.BooleanField(verbose_name="Veröffentlicht", default=False)
    answer_text = models.TextField(blank=True, help_text="Bei den Antworten funktioniert auch HTML-Syntax!<br> Aus Gründen des verwendeten CSS-Frameworks muss der Tag <strong>&lt;ul&gt;</strong> die CSS-Klasse <em>browser-default</em> besitzen!")

    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, blank=True)

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