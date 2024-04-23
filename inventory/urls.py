from django.urls import path

from . import views

urlpatterns = [
    path("", views.inventory_user, name="inventory-user"),
    path("admin", views.inventory_admin, name="inventory-admin"),
    path("user/", views.dashboard_user, name="dashboard-user"),
    path("basket/", views.basket, name="basket"),
    path("login/", views.login_view, name="user-login"),
    path("register/", views.register_view, name="register-view"),
    path("add-to-basket/<int:item_id>/", views.add_item, name="add-item")
]
