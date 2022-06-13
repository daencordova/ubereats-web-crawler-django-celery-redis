import logging

from ..city.models import CityModel
from .models import CategoryModel, CityCategoryModel


LOGGER = logging.getLogger(__name__)


class CategoryPersistence:
    @classmethod
    def save(cls, row):
        try:
            model = CategoryModel()
            model.category = row["category"]
            model.slug = row["slug"]
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, category):
        return CategoryModel.objects.filter(category=category).exists()

    @classmethod
    def get(cls, city_id):
        query = f"""
            SELECT
                ubereats_category.category_id,
                ubereats_category.slug AS category_slug
            FROM ubereats_category
            JOIN ubereats_city_category ON ubereats_category.category_id = ubereats_city_category.category_id
            JOIN ubereats_city ON ubereats_city_category.city_id = ubereats_city.city_id
            JOIN ubereats_location ON ubereats_city.location_id = ubereats_city.location_id
            WHERE ubereats_location.enabled = True
            AND ubereats_city_category.city_id = '{city_id}'
            AND ubereats_city.enabled = True
            AND ubereats_category.enabled = True
        """

        return CategoryModel.objects.raw(query.format(city_id=city_id))

    @classmethod
    def get_id(cls, category):
        category = (
            CategoryModel.objects.filter(category=category)
            .values("category_id")
            .first()
        )
        return category["category_id"]


class CityCategoryPersistence:
    @classmethod
    def save(cls, row):
        try:
            model = CityCategoryModel()
            model.city = CityModel.objects.get(pk=row["city_id"])
            model.category = CategoryModel.objects.get(pk=row["category_id"])
            model.save()

            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    @classmethod
    def exists(cls, city_id, category_id):
        return CityCategoryModel.objects.filter(
            city_id=city_id, category_id=category_id
        ).exists()
