from django.contrib import admin
from faq.models import Question, FAQQuestion

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "user", "answered")
    list_filter = ("answered",)

admin.site.register(Question, QuestionAdmin)

class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "icon", "answered")

admin.site.register(FAQQuestion, FAQQuestionAdmin)