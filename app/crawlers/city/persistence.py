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

    @classmethod
    def exists(cls, url):
        return CityModel.objects.filter(url=url).exists()

    @classmethod
    def get(cls):
        query = f"""
            SELECT
                ubereats_location.slug AS location_slug,
                ubereats_city.city_id,
                ubereats_city.slug AS city_slug
            FROM ubereats_city
            JOIN ubereats_location ON ubereats_city.location_id = ubereats_location.location_id
            WHERE ubereats_location.enabled = True AND ubereats_city.enabled = True
        """

        return CityModel.objects.raw(query)
