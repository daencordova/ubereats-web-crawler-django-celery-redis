from django.contrib import admin

from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "slug", "enabled", "created"]
    list_filter = ["category", "enabled"]
    list_editable = ["enabled"]
    actions = ["make_categories_enabled", "make_categories_disabled"]

    def make_categories_enabled(self, request, queryset):
        queryset.update(enabled=True)

    make_categories_enabled.short_description = "Mark selected Categories as enabled"

    def make_categories_disabled(self, request, queryset):
        queryset.update(enabled=False)

    make_categories_disabled.short_description = "Mark selected Categories as disabled"
