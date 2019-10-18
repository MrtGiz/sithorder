from django.contrib import admin

from .models import Planet, Sith, TestQuestions, Test, Recruit, TestAnswers

# Register your models here.

admin.site.register(Planet)


class RecruitInline(admin.TabularInline):
    model = Recruit


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    ordering = ['name']
    inlines = [RecruitInline, ]
    list_display = ['name', 'planet', 'shadow_hand_count']


@admin.register(TestQuestions)
class TestAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['question', 'is_used_in_test']


class TestAnswersInline(admin.TabularInline):
    model = TestAnswers
    readonly_fields = ['answer', 'to_question']


@admin.register(Test)
class TestsAdmin(admin.ModelAdmin):
    ordering = ['id']
    readonly_fields = ['recruit', ]
    inlines = [TestAnswersInline]
    exclude = ['questions']
    list_display = ['id', 'recruit']
