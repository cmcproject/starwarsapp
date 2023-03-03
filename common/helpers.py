import csv
from datetime import datetime
from django.conf import settings
from django.utils.dateparse import parse_datetime

from common.services.star_wars import StarWarsService
from people.models import PeopleDataset


def get_people_data():
    """
    Get data and peform updates
    """
    people = StarWarsService().get_people()

    # Update hometown and date
    homeworld_mapping = dict()
    for p in people:
        url = p.get("homeworld")
        idx = url.split("/")[-2]
        if idx not in homeworld_mapping.keys():
            name = StarWarsService().get_planet(idx).get("name")
            homeworld_mapping[idx] = name
        p["homeworld"] = homeworld_mapping[idx]
        p["date"] = parse_datetime(p["edited"]).strftime("%Y-%m-%d")

    return people


def write_to_csv(people, file_name):
    """
    Write to csv
    :people: People list
    :file_name: File name
    """
    with open(f"{settings.STORAGE_DIR}/{file_name}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, people[0].keys())
        writer.writeheader()
        writer.writerows(people)


def save_data():
    """
    Save data to database and generate CSV
    """
    date_created = f"{datetime.now()}".replace(".", "-").replace(":", "-").replace(" ", "-")
    p = PeopleDataset()
    p.name = f"output-{date_created}"
    p.save()

    people = get_people_data()
    write_to_csv(people, p.id)
