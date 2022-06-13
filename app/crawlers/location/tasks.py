import logging
import json

from celery import shared_task, states
from celery.exceptions import Ignore

from ..common.fetcher import Fetcher
from ..common.parser import Parser
from ..common.tasks import start_log_error_task

from .models import LocationModel
from .persistence import LocationPersistence


fetcher = Fetcher()

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.ubereats.com"


@shared_task(name="start_location_task")
def start_location_task():
    url = f"{BASE_URL}/location"
    bsoup = Parser.get_bsoup(fetcher, url)

    if not bsoup:
        return False

    content = bsoup.find("main", id="main-content")
    a_list = content.find_all("a")

    for a_tag in a_list:
        parcial = a_tag.attrs["href"]

        if not parcial.endswith("/location"):
            continue

        crawl_location_content.s(
            country_name=a_tag.get_text(), country_url=BASE_URL + parcial
        ).on_error(start_log_error_task.s()).apply_async()


@shared_task(bind=True, name="crawl_location_content")
def crawl_location_content(self, country_name, country_url):
    try:
        bsoup = Parser.get_bsoup(fetcher, country_url)

        if not bsoup:
            return False

        content = bsoup.find("main", id="main-content")
        a_list = content.find_all("a")

        data = []

        for a_tag in a_list:
            parcial = a_tag.attrs["href"]

            if "/region" not in parcial:
                continue

            state_name = a_tag.get_text()
            url_vals = parcial.split("/")

            if LocationPersistence.exists(country_name, state_name):
                LOGGER.info(f"location.[{country_name}|{state_name}] already exists...")
                continue

            slug = url_vals[1] if len(url_vals) == 4 else None
            row = {"country": country_name, "state": state_name, "slug": slug}
            model = LocationPersistence.add(row)

            if model:
                data.append(model)

        LocationModel.objects.bulk_create(data)
        return "status: OK, rows: %s" % len(data)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()
