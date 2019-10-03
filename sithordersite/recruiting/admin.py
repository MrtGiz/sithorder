from django.contrib import admin

from .models import Planet, Sith, TestQuestions, Test, Recruit, TestAnswers

# Register your models here.

admin.site.register(Planet)


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'planet', 'shadow_hand_count']


@admin.register(TestQuestions)
class TestAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['question', 'is_used_in_test']


class QuestionsInline(admin.TabularInline):
    model = TestQuestions


@admin.register(Test)
class TestsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'recruit']


class TestInline(admin.TabularInline):
    model = Test
    fields = ['questions']


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name', 'planet', 'age', 'email', 'shadow_hand_rank', 'master']
    inlines = [TestInline]


class TestStackedInline(admin.StackedInline):
    model = Test
    fields = ['questions']


@admin.register(TestAnswers)
class AnswersAdmin(admin.ModelAdmin):
    ordering = ['to_question']
    # inlines = [TestStackedInline]
