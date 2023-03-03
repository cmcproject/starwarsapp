import logging
import petl as etl
from threading import Thread
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

from people.const import CountingStatus
from common.helpers import save_data
from people.models import PeopleDataset

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_datasets(request):
    """
    Get all datasets
    """
    datasets = PeopleDataset.objects.all()

    context = {"datasets": datasets}

    return render(request, "datasets.html", context=context)


def download_data(request):
    """
    Download data (simulate celery worker)
    """
    Thread(target=save_data).start()

    return render(request, "download.html")


def get_people(request, id):
    """
    Get people by dataset id
    """
    dataset = get_object_or_404(PeopleDataset, pk=id)

    people = col1 = col2 = None
    counting_status = CountingStatus.DISABLED

    try:
        table = etl.fromcsv(f"{settings.STORAGE_DIR}/{dataset.id}.csv")
        people = list(table.dicts())
    except FileNotFoundError:
        logger.warn("Data is not available yet!")

    if request.GET.get("col1") and request.GET.get("col2"):
        col1 = request.GET.get("col1")
        col2 = request.GET.get("col2")
        columns = people[0].keys()
        if col1 in columns and col2 in columns:
            table = etl.aggregate(table, key=(col1, col2), aggregation={"count": len})
            people = list(table.dicts())

            new_people = []
            for p in people:
                d = {"col1": p.get(col1), "col2": p.get(col2), "count": p.get("count")}
                new_people.append(d)
            people = new_people
            counting_status = CountingStatus.ENABLED

        else:
            logger.error("Invalid columns")
            counting_status = CountingStatus.WRONG_PARAMS

    if request.GET.get("number_per_page"):
        number_per_page = int(request.GET.get("number_per_page"))
        people = people[:number_per_page]

    context = {"people": people, "counting_status": counting_status, "col1": col1, "col2": col2}

    return render(request, "people.html", context=context)
