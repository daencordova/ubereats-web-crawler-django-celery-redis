import logging
import json

from celery import shared_task, states
from celery.exceptions import Ignore

from ..common.fetcher import Fetcher
from ..common.parser import Parser
from ..common.tasks import start_log_error_task

from ..common.cache import RestaurantCache, CategoryRestaurantCache
from ..city.persistence import CityPersistence
from ..category.persistence import CategoryPersistence

from .persistence import RestaurantPersistence, CategoryRestaurantPersistence


fetcher = Fetcher()

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.ubereats.com"


@shared_task(name="start_restaurant_task")
def start_restaurant_task():
    RestaurantPersistence.set_entries_cache()
    CategoryRestaurantPersistence.set_entries_cache()
    cities = CityPersistence.get()

    for city in cities:
        categories = CategoryPersistence.get(city.city_id)

        for category in categories:
            crawl_restaurant_content.s(
                city.location_slug,
                city.city_id,
                city.city_slug,
                category.category_id,
                category.category_slug,
            ).on_error(start_log_error_task.s()).apply_async()


@shared_task(bind=True, name="crawl_restaurant_content")
def crawl_restaurant_content(
    self, location_slug, city_id, city_slug, category_id, category_slug
):
    try:
        url = f"{BASE_URL}/{location_slug}/category/{city_slug}/{category_slug}"

        if not location_slug:
            url = "{BASE_URL}/category/{city_slug}/{category_slug}"

        bsoup = Parser.get_bsoup(fetcher, url)

        if not bsoup:
            return False

        content = bsoup.find("main", id="main-content")
        a_list = content.find_all("a")

        if not a_list:
            return False

        data = []

        for a_tag in a_list:
            parcial = a_tag.attrs["href"]

            if "/restaurant" not in parcial:
                continue

            restaurant_url = BASE_URL + parcial

            if RestaurantCache.add_member(restaurant_url):
                row = {"city_id": city_id, "url": restaurant_url}
                result = RestaurantPersistence.save(row)
                data.append(result)

            restaurant_id = RestaurantPersistence.get_id(restaurant_url)

            if CategoryRestaurantCache.add_member(category_id, restaurant_id):
                row = {"category_id": category_id, "restaurant_id": restaurant_id}
                CategoryRestaurantPersistence.save(row)

        return "status: OK, rows: %s" % len(data)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()


@shared_task(name="start_restaurant_detail_task")
def start_restaurant_detail_task():
    restaurants = RestaurantPersistence.get()

    for restaurant in restaurants:
        crawl_restaurant_detail_content.s(restaurant.url).on_error(
            start_log_error_task.s()
        ).apply_async()


@shared_task(bind=True, name="crawl_restaurant_detail_content")
def crawl_restaurant_detail_content(self, restaurant_url):
    try:
        bsoup = Parser.get_bsoup(fetcher, restaurant_url)

        if not bsoup:
            RestaurantPersistence.disable(restaurant_url)
            return False

        content = bsoup.find("main", id="main-content")
        scripts = content.find_all("script")

        json_data = json.loads(scripts[0].text)

        data = {
            "url": restaurant_url,
            "restaurant": json_data.get("name"),
            "restaurant_type": json_data.get("@type"),
            "address_locality": json_data.get("address", {}).get("addressLocality"),
            "address_region": json_data.get("address", {}).get("addressRegion"),
            "postal_code": json_data.get("address", {}).get("postalCode"),
            "address_country": json_data.get("address", {}).get("addressCountry"),
            "street_address": json_data.get("address", {}).get("streetAddress"),
            "latitude": json_data.get("geo", {}).get("latitude"),
            "longitude": json_data.get("geo", {}).get("longitude"),
            "telephone": json_data.get("telephone"),
            "rating_value": json_data.get("aggregateRating", {}).get("ratingValue"),
            "review_count": json_data.get("aggregateRating", {}).get("reviewCount"),
            "opening_hours": json_data.get("openingHoursSpecification"),
            "data": json_data,
        }

        result = RestaurantPersistence.update(data)
        return "status: OK, rows: %s" % int(result)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()
