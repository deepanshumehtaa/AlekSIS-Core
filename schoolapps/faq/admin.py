from django.contrib import admin
from faq.models import Question, FAQQuestion

# Register your models here.
def show(modeladmin, request, queryset):
    queryset.update(show=True)
show.short_description = "Ausgewählte Fragen veröffentlichen"

def hide(modeladmin, request, queryset):
    queryset.update(show=False)
hide.short_description = "Ausgewählte Fragen nicht mehr veröffentlichen"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "user", "answered")
    list_filter = ("answered",)

admin.site.register(Question, QuestionAdmin)

class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "icon", "show")
    actions = [show, hide]

admin.site.register(FAQQuestion, FAQQuestionAdmin)