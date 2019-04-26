from django.contrib import admin
from faq.models import Question, Answer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "user", "answered")
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)