from django.contrib import admin

from .models import MenuModel


@admin.register(MenuModel)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "menu",
        "description",
        "price",
        "currency",
        "status",
        "restaurant_url",
        "created",
        "updated",
    ]
    list_filter = ["menu", "status", "restaurant_url"]
    list_editable = ["status"]
