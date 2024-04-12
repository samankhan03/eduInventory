from django.urls import path

from . import views

urlpatterns = [
    path("", views.inventory_user, name="inventory-user"),
    path("admin", views.inventory_admin, name="inventory-admin"),
]