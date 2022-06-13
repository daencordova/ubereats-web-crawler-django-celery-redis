import logging

from celery import shared_task, states
from celery.exceptions import Ignore

from ..common.fetcher import Fetcher
from ..common.parser import Parser
from ..common.tasks import start_log_error_task

from ..location.persistence import LocationPersistence
from .persistence import CityPersistence


fetcher = Fetcher()

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.ubereats.com"


@shared_task(name="start_city_task")
def start_city_task():
    state_name = None
    locations = LocationPersistence.get()

    for location in locations:
        url = f"{BASE_URL}/{location.slug}/location"

        if not location.slug:
            url = f"{BASE_URL}/location"

        bsoup = Parser.get_bsoup(fetcher, url)

        if not bsoup:
            return False

        content = bsoup.find("main", id="main-content")
        a_list = content.find_all("a")

        for a_tag in a_list:
            parcial = a_tag.attrs["href"]

            if "/region" in parcial:
                state_name = a_tag.get_text()

            if "/city" in parcial and location.state == state_name:
                city_name = a_tag.get_text()
                location_id = location.location_id

                crawl_city_content.s(location_id, city_name, parcial).on_error(
                    start_log_error_task.s()
                ).apply_async()


@shared_task(bind=True, name="crawl_city_content")
def crawl_city_content(self, location_id, city_name, parcial):
    try:
        city_url = BASE_URL + parcial

        if CityPersistence.exists(city_url):
            LOGGER.info(f"city.[{city_url}] already exists...")
            return False

        slug = parcial.split("/")[-1]

        row = {
            "location_id": location_id,
            "city": city_name,
            "slug": slug,
            "url": city_url,
        }

        result = CityPersistence.save(row)
        return "status: OK, rows: %s" % int(result)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()
