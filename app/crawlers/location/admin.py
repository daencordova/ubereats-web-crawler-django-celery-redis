from django.contrib import admin

from .models import LocationModel


@admin.register(LocationModel)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["country", "state", "created", "enabled"]
    list_filter = ["country", "enabled"]
    list_editable = ["enabled"]
    actions = ["make_locations_enabled", "make_locations_disabled"]

    def make_locations_enabled(self, request, queryset):
        queryset.update(enabled=True)

    make_locations_enabled.short_description = "Mark selected Locations as enabled"

    def make_locations_disabled(self, request, queryset):
        queryset.update(enabled=False)

    make_locations_disabled.short_description = "Mark selected Locations as disabled"
