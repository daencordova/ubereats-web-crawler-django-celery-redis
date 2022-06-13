import logging
import json

from celery import shared_task, states
from celery.exceptions import Ignore

from ..common.fetcher import Fetcher
from ..common.parser import Parser
from ..common.tasks import start_log_error_task

from ..city.persistence import CityPersistence
from .persistence import CategoryPersistence, CityCategoryPersistence

fetcher = Fetcher()

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.ubereats.com"


@shared_task(name="start_category_task")
def start_category_task():
    cities = CityPersistence.get()

    for city in cities:
        crawl_category_content.s(
            city.location_slug, city.city_id, city.city_slug
        ).on_error(start_log_error_task.s()).apply_async()


@shared_task(bind=True, name="crawl_category_content")
def crawl_category_content(self, location_slug, city_id, city_slug):
    try:
        url = f"{BASE_URL}/{location_slug}/category/{city_slug}"

        if not location_slug:
            url = "{BASE_URL}/category/{city_slug}"

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
            category_name = a_tag.get_text()

            if "/category" not in parcial:
                continue

            if not CategoryPersistence.exists(category_name):
                row = {"category": category_name, "slug": parcial.split("/")[-1]}
                result = CategoryPersistence.save(row)
                data.append(result)

            category_id = CategoryPersistence.get_id(category_name)

            if not CityCategoryPersistence.exists(city_id, category_id):
                row = {
                    "city_id": city_id,
                    "category_id": category_id,
                }
                CityCategoryPersistence.save(row)

        return "status: OK, rows: %s" % len(data)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()
