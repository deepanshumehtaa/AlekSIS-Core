from django.contrib import admin
from faq.models import FAQQuestion, FAQSection
from django.utils.html import format_html


def show(modeladmin, request, queryset):
    queryset.update(show=True)


show.short_description = "Ausgewählte Fragen veröffentlichen"


def hide(modeladmin, request, queryset):
    queryset.update(show=False)


hide.short_description = "Ausgewählte Fragen nicht mehr veröffentlichen"


class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "_icon")

    class Media:
        css = {
            'all': ('/static/css/materialdesignicons-webfont/material-icons.css',)
        }

    def _icon(self, obj):
        return format_html(u'<i style="color: {};" class="material-icons">{}<i/>', obj.icon_color, obj.icon)


class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "section", "_icon", "show")
    actions = [show, hide]

    class Media:
        css = {
            'all': ('/static/css/materialdesignicons-webfont/material-icons.css',)
        }

    def _icon(self, obj):
        return format_html(u'<i class="material-icons">{}<i/>', obj.icon)


admin.site.register(FAQQuestion, FAQQuestionAdmin)
admin.site.register(FAQSection, FAQSectionAdmin)
