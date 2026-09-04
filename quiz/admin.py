from django.contrib import admin
from .models import Exam, Question, Choice


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['statement_short', 'exam']
    list_filter = ['exam']
    search_fields = ['statement']

    def statement_short(self, obj):
        return obj.statement[:50] + "..." if len(obj.statement) > 50 else obj.statement
    statement_short.short_description = "Enunciado"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'question']
    list_filter = ['is_correct', 'question']
    search_fields = ['text']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question')