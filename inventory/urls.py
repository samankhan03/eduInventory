from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="inventory-user"),
    path("admin", views.admin, name="inventory-admin"),
]