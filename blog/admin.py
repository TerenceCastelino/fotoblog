from django.contrib import admin
from .models import Photo, Blog

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "uploader", "caption", "date_created")
    search_fields = ("caption",)
    list_filter = ("date_created", "uploader")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "word_count", "date_created", "starred")
    fields = ("photo", "title", "content", "author", "starred", "word_count")
    readonly_fields = ("word_count",)
