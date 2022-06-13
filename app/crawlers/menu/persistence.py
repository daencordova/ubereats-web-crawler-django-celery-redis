import logging

from ..restaurant.models import RestaurantModel
from .models import MenuModel


LOGGER = logging.getLogger(__name__)


class MenuPersistence:
    @classmethod
    def add(cls, row):
        try:
            model = MenuModel()
            model.restaurant = RestaurantModel.objects.get(pk=row["restaurant_id"])
            model.menu = row["menu"]
            model.description = row["description"]
            model.price = float(row["price"]) / 100
            model.currency = row["currency"]
            model.restaurant_url = row["restaurant_url"]
            model.status = True
            model.data = row["data"]

            return model
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def update(cls, row):
        try:
            model = MenuModel.objects.filter(
                restaurant_id=row["restaurant_id"], menu=row["menu"]
            )
            model.description = row["description"]
            model.price = float(row["price"]) / 100
            model.currency = row["currency"]
            model.data = row["data"]
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, restaurant_id, menu):
        return MenuModel.objects.filter(restaurant_id=restaurant_id, menu=menu).exists()
