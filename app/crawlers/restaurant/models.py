import uuid

from django.db import models

from ..city.models import CityModel
from ..category.models import CategoryModel


class RestaurantModel(models.Model):

    restaurant_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    city = models.ForeignKey(CityModel, on_delete=models.RESTRICT)
    restaurant = models.CharField(max_length=150, null=True, blank=True)
    restaurant_type = models.CharField(max_length=150, null=True, blank=True)
    address_locality = models.CharField(max_length=200, null=True, blank=True)
    address_region = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    address_country = models.CharField(max_length=200, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    rating_value = models.CharField(max_length=200, null=True, blank=True)
    review_count = models.CharField(max_length=200, null=True, blank=True)
    opening_hours = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=250, null=False)
    status = models.BooleanField(default=True)
    data = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ubereats.restaurant <Id:{self.restaurant_id}> <Name:{self.restaurant}>"

    class Meta:
        db_table = "ubereats_restaurant"
        verbose_name_plural = "Restaurant"
        indexes = [models.indexes.Index(fields=["url"])]


class CategoryRestaurantModel(models.Model):

    category_restaurant_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT)
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.RESTRICT)

    def __str__(self):
        return f"ubereats.category_restaurant <Category Id:{self.category}> <Restaurant Id:{self.restaurant}>"

    class Meta:
        db_table = "ubereats_category_restaurant"
        verbose_name_plural = "CategoryRestaurant"
