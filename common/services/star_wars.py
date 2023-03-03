import logging
import math
import requests
from requests.exceptions import RequestException


LOG = logging.getLogger(__name__)


class StarWarsService:
    def __init__(self):
        self.url = "https://swapi.dev/api/"
        self.people_endpoint = "people"
        self.planets_endpoint = "planets"

    def get_people(self):
        # reduce the nb of requests by getting chunks of 10 people
        people_per_page = 10

        all_people = []
        try:
            url = f"{self.url}{self.people_endpoint}"
            response = requests.get(url)
            if str(response.status_code).startswith("2"):
                count = 20  # response.json().get("count")
                count = math.ceil(count / people_per_page)
                for idx in range(1, count + 1):
                    url = f"{self.url}{self.people_endpoint}/?page={idx}"
                    response = requests.get(url)

                    people = response.json().get("results")
                    all_people = all_people + people
        except RequestException as exc:
            msg = f"Getting people data failed due to {exc}"
            LOG.error(msg)

        return all_people

    def get_planet(self, idx):
        planet = None
        try:
            url = f"{self.url}{self.planets_endpoint}/{idx}"
            response = requests.get(url)
            if str(response.status_code).startswith("2"):
                planet = response.json()
        except RequestException as exc:
            msg = f"Getting planet data failed due to {exc}"
            LOG.error(msg)

        return planet
