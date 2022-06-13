import logging

from ..city.models import CityModel
from ..category.models import CategoryModel
from .models import RestaurantModel, CategoryRestaurantModel

from ..common.cache import RestaurantCache, CategoryRestaurantCache


LOGGER = logging.getLogger(__name__)


class RestaurantPersistence:
    @classmethod
    def save(cls, row):
        try:
            model = RestaurantModel()
            model.city = CityModel.objects.get(pk=row["city_id"])
            model.url = row["url"]
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def update(cls, row):
        try:
            model = RestaurantModel.objects.get(url=row["url"])
            model.restaurant = row["restaurant"]
            model.restaurant_type = row["restaurant_type"]
            model.address_locality = row["address_locality"]
            model.address_region = row["address_region"]
            model.postal_code = row["postal_code"]
            model.address_country = row["address_country"]
            model.street_address = row["street_address"]
            model.latitude = row["latitude"]
            model.longitude = row["longitude"]
            model.telephone = row["telephone"]
            model.rating_value = row["rating_value"]
            model.review_count = row["review_count"]
            model.opening_hours = row["opening_hours"]
            model.data = row["data"]
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def disable(cls, url):
        try:
            model = RestaurantModel.objects.get(url=url)
            model.status = False
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, url):
        return RestaurantModel.objects.filter(url=url).exists()

    @classmethod
    def set_entries_cache(cls):
        query = f"""
            SELECT
                ubereats_restaurant.restaurant_id,
                ubereats_restaurant.url
            FROM ubereats_restaurant
        """

        for restaurant in RestaurantModel.objects.raw(query):
            RestaurantCache.add_member(restaurant.url)

    @classmethod
    def get(cls):
        restaurants = RestaurantPersistence.count()
        extra = f"AND ubereats_restaurant.restaurant IS NULL" if restaurants > 0 else ""

        query = f"""
            SELECT
                ubereats_restaurant.restaurant_id,
                ubereats_restaurant.url
            FROM ubereats_restaurant
            JOIN ubereats_city ON ubereats_restaurant.city_id = ubereats_city.city_id
            JOIN ubereats_location ON ubereats_city.location_id = ubereats_location.location_id
            WHERE ubereats_location.enabled = True
            AND ubereats_city.enabled = True {extra}
        """

        return RestaurantModel.objects.raw(query)

    @classmethod
    def count(cls):
        return RestaurantModel.objects.filter(restaurant__isnull=True).count()

    @classmethod
    def get_id(cls, url):
        restaurant = (
            RestaurantModel.objects.filter(url=url).values("restaurant_id").first()
        )
        return restaurant["restaurant_id"]


class CategoryRestaurantPersistence:
    @classmethod
    def save(cls, row):
        try:
            model = CategoryRestaurantModel()
            model.category = CategoryModel.objects.get(pk=row["category_id"])
            model.restaurant = RestaurantModel.objects.get(pk=row["restaurant_id"])
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, category_id, restaurant_id):
        return CategoryRestaurantModel.objects.filter(
            category_id=category_id, restaurant_id=restaurant_id
        ).exists()

    @classmethod
    def set_entries_cache(cls):
        query = """
            SELECT
                ubereats_category_restaurant.category_restaurant_id,
                ubereats_category_restaurant.category_id,
                ubereats_category_restaurant.restaurant_id
            FROM ubereats_category_restaurant
        """

        for category_restaurant in CategoryRestaurantModel.objects.raw(query):
            CategoryRestaurantCache.add_member(
                category_restaurant.category_id, category_restaurant.restaurant_id
            )
