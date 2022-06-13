import os
import time
import logging
from random import randint, choice, randrange

import requests
from requests.exceptions import ConnectionError

from .items import USER_AGENTS


class Fetcher:

    MIN_DELAY = int(os.getenv("MIN_DELAY"))
    MAX_DELAY = int(os.getenv("MAX_DELAY"))

    def get_content(self, url):
        try:
            response = self.get_response(url)
            status_code = response.status_code

            logging.debug(f"Url: {url} <{status_code}>")

            if status_code == 200:
                return response.content
            elif status_code == 404:
                raise Exception(f"Got an HTTP 404 error code 'Page not found': {url}")
            elif status_code == 500:
                raise Exception("Got an HTTP 500 error code 'Internal Server Error'")
            else:
                raise Exception(f"Unknown error: {url}")
        except Exception as error:
            raise Exception(error)

    def get_response(self, url):
        attemps = 0

        while attemps < 3:
            try:
                attemps += 1
                time.sleep(randrange(self.MIN_DELAY, self.MAX_DELAY))

                return requests.get(
                    url, headers={"User-Agent": choice(USER_AGENTS)}, timeout=30
                )
            except (Exception, ConnectionError):
                logging.warning(
                    f"Attemp #{attemps}, request failed while connecting..."
                )
                time.sleep(randint(20, 30))

        raise Exception("No successful responses received until now, descarting...")
