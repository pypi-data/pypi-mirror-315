from django.contrib import admin

from .models import PageMetaOg


@admin.register(PageMetaOg)
class PageMetaOgAdmin(admin.ModelAdmin):
    ordering = ["page", "page__changed_date", "language"]
