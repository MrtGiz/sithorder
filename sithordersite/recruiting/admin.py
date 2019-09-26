from django.contrib import admin

from .models import Planet, Sith

# Register your models here.

admin.site.register(Planet)


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    list_display = ['name', 'planet', 'shadow_hand_count']
