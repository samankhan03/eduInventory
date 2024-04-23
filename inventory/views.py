from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from inventory.models import InventoryItem, BorrowedItem


def inventory_user(request):
    # Retrieve all InventoryItem objects from the database
    inventory_items = InventoryItem.objects.all()

    # Pass the inventory items to the template context
    return render(request, 'inventory_user.html', {'inventory_items': inventory_items})


def inventory_admin(request):
    return render(request, 'inventory_admin.html')


def dashboard_user(request):
    return render(request, 'dashboard_user.html')


def basket(request):
    inventory_items = InventoryItem.objects.all()
    return render(request, 'basket.html', {'inventory_items': inventory_items})


def admin(request):
    return HttpResponse('<p>hello </p>')


def add_item(request, item_id):
    if request.method == 'POST':
        item_id = int(item_id)
        # Get the user's session
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        # Retrieve the list of item IDs from the session or create an empty list if it doesn't exist
        item_ids = request.session.get('basket_items', [])
        # Add the new item ID to the list
        if item_id not in item_ids:
            item_ids.append(item_id)
        # Save the updated list back to the session
        request.session['basket_items'] = item_ids

        # Print the session data to the console for testing
        print("Basket items:")
        for id in item_ids:
            item = InventoryItem.objects.get(pk=id)
            print(f"ID: {item.id}, Name: {item.name}")

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Item added to basket successfully'})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'error': 'Invalid request method'})

def get_basket(request):
    if request.method == 'GET':
        # Get the list of item IDs from the session
        item_ids = request.session.get('basket_items', [])
        # Retrieve the items from the database using the IDs
        items = InventoryItem.objects.filter(id__in=item_ids)
        # Create BorrowedItem instances for each item
        for item in items:
            BorrowedItem.objects.create(user=request.user, item=item)
        # Clear the session
        request.session['basket_items'] = []
        # Render the basket page with the items
        return render(request, 'basket.html', {'items': items})
