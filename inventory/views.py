from django.shortcuts import render
from django.http import HttpResponse
from inventory.models import InventoryItem


def inventory_user(request):
    # Retrieve all InventoryItem objects from the database
    inventory_items = InventoryItem.objects.all()
    for inventory_item in inventory_items:
        if inventory_item.status == "nan":
            inventory_item.status = "Available"
    # Pass the inventory items to the template context
    return render(request, 'inventory_user.html', {'inventory_items': inventory_items})


def inventory_admin(request):
    return render(request, 'inventory_admin.html')


def admin(request):
    return HttpResponse('<p>hello </p>')
