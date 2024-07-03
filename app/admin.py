from django.contrib import admin
from .models import Test, Question, Answer, CustomUser

admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(CustomUser)


class ChildQuestionAnswer(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChildQuestionAnswer,
    ]

admin.site.register(Question, QuestionAdmin)
