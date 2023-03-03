from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_datasets, name="datasets"),
    path("datasets/<str:id>", views.get_people, name="people"),
    path("download", views.download_data, name="download"),
]
