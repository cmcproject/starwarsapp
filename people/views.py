import logging
import petl as etl
from threading import Thread
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

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
    count_exists = False

    try:
        table = etl.fromcsv(f"{settings.STORAGE_DIR}/{dataset.id}.csv")
        people = list(table.dicts())
    except FileNotFoundError:
        logger.warn("Data is not available yet!")

    context = {"people": people, "count_exists": False}
    if request.GET.get("col1") and request.GET.get("col2"):
        col1 = request.GET.get("col1")
        col2 = request.GET.get("col2")
        table = etl.aggregate(table, key=(col1, col2), aggregation={"count": len})
        people = list(table.dicts())

        new_people = []
        for p in people:
            d = {"col1": p.get(col1), "col2": p.get(col2), "count": p.get("count")}
            new_people.append(d)
        people = new_people

    if request.GET.get("number_per_page"):
        number_per_page = int(request.GET.get("number_per_page"))
        people = people[:number_per_page]

    context = {"people": people, "count_exists": count_exists, "col1": col1, "col2": col2}

    return render(request, "people.html", context=context)
