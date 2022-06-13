import uuid

from django.db import models

from ..location.models import LocationModel


class CityModel(models.Model):

    city_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(LocationModel, on_delete=models.RESTRICT)
    city = models.CharField(max_length=100, null=True)
    slug = models.CharField(max_length=100, null=True)
    url = models.URLField(max_length=150, null=False)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ubereats.city <Id:{self.city_id}> <Name:{self.city}>"

    class Meta:
        db_table = "ubereats_city"
        verbose_name_plural = "City"
        indexes = [models.indexes.Index(fields=["url"])]
