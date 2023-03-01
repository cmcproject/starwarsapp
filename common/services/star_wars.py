import logging
import requests
from requests.exceptions import RequestException


LOG = logging.getLogger(__name__)


class StarWarsService:
    def __init__(self):
        self.url = "https://swapi.dev/api/"
        self.people_endpoint = "people"

    def get_people(self):
        all_people = []
        try:
            url = f"{self.url}{self.people_endpoint}"
            response = requests.get(url, timeout=10)
            if str(response.status_code).startswith("2"):
                # reduce the nb of request by getting chunks of 10 people
                count = int(response.json().get("count") / 10)
                for idx in range(count):
                    url = f"{self.url}{self.people_endpoint}/?page={idx}"
                    people = response.json().get("results")
                    all_people = all_people + people

                # TODO: get homewold name instead of url
                # # update homeworld with the value
                # for p in all_people:
                #     name = requests.get(p.get("homeworld"), timeout=10).json().get("name")
                #     p["homeworld"] = name

        except RequestException as exc:
            msg = f"Getting applicant tasks data failed due to {exc}"
            LOG.error(msg)

        return all_people

