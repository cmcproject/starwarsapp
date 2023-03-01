import logging
import time
import csv
from django.shortcuts import render
from common.services.star_wars import StarWarsService
from django.conf import settings


# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    people = StarWarsService().get_people()
    logger.info(len(people))

    time_str = f"{time.time()}".replace(".", "-")
    with open(f'{settings.STORAGE_DIR}/output-{time_str}.csv', 'w', newline='') as file:
         writer = csv.DictWriter(file, people[0].keys())
         writer.writeheader()
         writer.writerows(people)

    context = {"people": people}

    return render(request, 'index.html', context=context)
