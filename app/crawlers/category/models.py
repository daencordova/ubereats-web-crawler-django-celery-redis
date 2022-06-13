import uuid

from django.db import models

from ..city.models import CityModel


class CategoryModel(models.Model):

    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=150, null=True)
    slug = models.CharField(max_length=100, null=True)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ubereats.category <Id:{self.category_id}> <Name:{self.category}>"

    class Meta:
        db_table = "ubereats_category"
        verbose_name_plural = "Category"


class CityCategoryModel(models.Model):

    city_category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    city = models.ForeignKey(CityModel, on_delete=models.RESTRICT)
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT)

    def __str__(self):
        return f"ubereats.city_category <City Id:{self.city}> <Category Id:{self.category}>"

    class Meta:
        db_table = "ubereats_city_category"
        verbose_name_plural = "CityCategory"
