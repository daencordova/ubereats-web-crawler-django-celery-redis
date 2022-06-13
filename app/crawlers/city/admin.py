from django.contrib import admin

from .models import CityModel


@admin.register(CityModel)
class CityAdmin(admin.ModelAdmin):
    list_display = ["city", "slug", "url", "enabled", "created"]
    list_filter = ["city", "enabled"]
    list_editable = ["enabled"]
    actions = ["make_cities_enabled", "make_cities_disabled"]

    def make_cities_enabled(self, request, queryset):
        queryset.update(enabled=True)

    make_cities_enabled.short_description = "Mark selected Cities as enabled"

    def make_cities_disabled(self, request, queryset):
        queryset.update(enabled=False)

    make_cities_disabled.short_description = "Mark selected Cities as disabled"
