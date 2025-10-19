from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("api/test_retrieval/", views.test_retrieval, name="test_retrieval"),
]