import uuid

from django.db import models

from ..restaurant.models import RestaurantModel


class MenuModel(models.Model):

    menu_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.RESTRICT)
    menu = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    price = models.FloatField(max_length=150, null=True, default=0)
    currency = models.CharField(max_length=5, null=True)
    status = models.BooleanField(default=True)
    restaurant_url = models.URLField(max_length=250, null=False)
    data = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ubereats.menu <Id:{self.menu_id}> <Name:{self.menu}>"

    class Meta:
        db_table = "ubereats_menu"
        verbose_name_plural = "Menu"
