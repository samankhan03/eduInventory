from django.urls import path

from . import views

urlpatterns = [
    path("", views.inventory_user, name="inventory-user"),
    path("user/", views.dashboard_user, name="dashboard-user"),
    path("basket/", views.basket, name="basket"),
    path("login/", views.login_view, name="user-login"),
    path("register/", views.register_view, name="register-view"),
    path("add-to-basket/<int:item_id>/", views.add_item, name="add-item"),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('reserve-all-items/', views.reserve_all_items, name='reserve-all-items'),
    path('logout/', views.logout_view, name='logout'),
    path('inventory_report/', views.generate_inventory_pdf, name='inventory_report'),
    path('usage_history_report/', views.generate_usage_history_pdf, name='usage_history_report'),
    path('overdue_items_report/', views.generate_overdue_items_pdf, name='overdue_items_report'),
    path('admin-login/', views.generate_overdue_items_pdf, name='overdue_items_report'),
    path('main-page/', views.main_page, name='main-page'),
]
