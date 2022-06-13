from django.contrib import admin

from .models import RestaurantModel


@admin.register(RestaurantModel)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "restaurant",
        "address_locality",
        "street_address",
        "url",
        "status",
        "created",
        "updated",
    ]
    list_filter = ["address_locality", "status"]
    list_editable = ["status"]
