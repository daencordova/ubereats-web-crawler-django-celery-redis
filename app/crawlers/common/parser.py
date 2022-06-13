import logging

from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    def get_bsoup(request, url):
        try:
            html = request.get_content(url)

            if html:
                bsoup = BeautifulSoup(html, "html.parser")
                logging.debug("Returning bsoup...")
                return bsoup
        except Exception as error:
            logging.error(error)

        return None
