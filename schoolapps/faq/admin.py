from django.contrib import admin
from django import forms
from faq.models import Question, FAQQuestion, FAQAnswer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "user", "answered")

admin.site.register(Question, QuestionAdmin)

# class FAQQuestionForm(forms.ModelForm):
#     question_text = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = FAQQuestion
#
class FAQQuestionAdmin(admin.ModelAdmin):
    #form = FAQQuestionForm
    list_display = ("question_text", "icon", "answered")

admin.site.register(FAQQuestion, FAQQuestionAdmin)
admin.site.register(FAQAnswer)