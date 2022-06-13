import logging

from .models import CityModel
from ..location.models import LocationModel


LOGGER = logging.getLogger(__name__)


class CityPersistence:
    @classmethod
    def save(cls, row):
        try:
            model = CityModel()
            model.location = LocationModel.objects.get(pk=row["location_id"])
            model.city = row["city"]
            model.slug = row["slug"]
            model.url = row["url"]
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False
