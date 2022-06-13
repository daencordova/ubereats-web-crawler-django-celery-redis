import logging
import json

from celery import shared_task, states
from celery.exceptions import Ignore

from ..common.fetcher import Fetcher
from ..common.parser import Parser
from ..common.tasks import start_log_error_task

from .models import MenuModel
from ..restaurant.persistence import RestaurantPersistence
from .persistence import MenuPersistence


fetcher = Fetcher()

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.ubereats.com"


@shared_task(name="start_menu_task")
def start_menu_task():
    restaurants = RestaurantPersistence.get()

    for restaurant in restaurants:
        crawl_menu_content.s(restaurant.restaurant_id, restaurant.url).on_error(
            start_log_error_task.s()
        ).apply_async()


@shared_task(bind=True, name="crawl_menu_content")
def crawl_menu_content(self, restaurant_id, restaurant_url):
    try:
        bsoup = Parser.get_bsoup(fetcher, restaurant_url)

        if not bsoup:
            return False

        content = bsoup.find("main", id="main-content")
        scripts = content.find_all("script")

        json_data = json.loads(scripts[0].text)

        if not json_data:
            return False

        has_menu = json_data.get("hasMenu", {})

        if not has_menu:
            return False

        data = []

        menu_section = has_menu.get("hasMenuSection", [])

        for menu in menu_section:
            menu_item = menu.get("hasMenuItem")

            for meal in menu_item:
                if not MenuPersistence.exists(restaurant_id, meal.get("name")):
                    row = {
                        "restaurant_id": restaurant_id,
                        "menu": meal.get("name"),
                        "description": meal.get("description"),
                        "price": meal.get("offers", {}).get("price", 0),
                        "currency": meal.get("offers", {}).get("priceCurrency"),
                        "restaurant_url": restaurant_url,
                        "data": menu_item,
                    }

                    model = MenuPersistence.add(row)

                    if model:
                        data.append(model)
                else:
                    MenuPersistence.update(row)

        MenuModel.objects.bulk_create(data)
        return "status: OK, rows: %s" % len(data)
    except Exception as error:
        LOGGER.exception(error)

    self.update_state(state=states.FAILURE, meta={"status": "FAILED"})
    raise Ignore()
