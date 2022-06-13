import logging

from .models import LocationModel


LOGGER = logging.getLogger(__name__)


class LocationPersistence:
    @classmethod
    def add(cls, row):
        try:
            model = LocationModel()
            model.country = row["country"]
            model.state = row["state"]
            model.slug = row["slug"]

            return model
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, country, state):
        return LocationModel.objects.filter(country=country, state=state).exists()

    @classmethod
    def get(cls):
        query = f"""
            SELECT
                ubereats_location.location_id,
                ubereats_location.state,
                ubereats_location.slug
            FROM ubereats_location
            WHERE ubereats_location.enabled = True
        """

        return LocationModel.objects.raw(query)
