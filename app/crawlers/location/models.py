import uuid

from django.db import models


class LocationModel(models.Model):

    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    slug = models.CharField(max_length=100, null=True)
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ubereats.location <Id:{self.location_id}> <Name:{self.state}>"

    class Meta:
        db_table = f"ubereats_location"
        verbose_name_plural = "Location"
