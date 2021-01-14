from django.contrib import admin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('session',)
    list_display = (
        'session',
        'side',
        'temperature',
        'error'
    )
