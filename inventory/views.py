from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from .models import InventoryItem, Basket
from .models import InventoryItem

# creating views
from .models import *
from .forms import CreateUserForm


def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was created for " + form.cleaned_data['username'])

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard-user')

    context = {}
    return render(request, 'loginpage.html', context)


def login_required(args):
    pass


# @login_required
def dashboard(request):
    user = request.user  # Retrieve authenticated user
    user_profile = User.objects.get(user=user)  # Query user profile data from your database
    context = {
        'user_profile': user_profile,
        # Add more context data as needed
    }
    return render(request, 'dashboard.html', context)


def inventory_user(request):
    # Retrieve all InventoryItem objects from the database
    inventory_items = InventoryItem.objects.all()

    # Pass the inventory items to the template context
    return render(request, 'inventory_user.html', {'inventory_items': inventory_items})


def inventory_admin(request):
    return render(request, 'inventory_admin.html')


def login_page(request):
    return render(request, 'loginpage.html')


def dashboard_user(request):
    basket_items = Basket.objects.all()
    return render(request, 'dashboard_user.html', {'basket':basket_items})




def basket(request):
    basket_items = Basket.objects.all()

    return render(request, 'basket.html', {'basket': basket_items})


def admin(request):
    return HttpResponse('<p>hello </p>')


def add_item(request, item_id):
    if request.method == 'POST':
        item_id = int(item_id)
        # Check if the item already exists in the basket
        basket_item = Basket.objects.filter(user=request.user, inventory_item_id=item_id).first()

        if basket_item:
            # If the item exists, increment its quantity by 1
            basket_item.quantity += 1
            basket_item.save()
        else:
            # If the item doesn't exist, create a new entry in the basket with quantity 1
            inventory_item = get_object_or_404(InventoryItem, pk=item_id)
            basket_item = Basket.objects.create(user=request.user, inventory_item=inventory_item, quantity=1)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Item added to basket successfully'})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'error': 'Invalid request method'})
    # item = get_object_or_404(InventoryItem, pk=item_id)
    #
    # # Retrieve the current user
    # user = request.user
    #
    # # Create a new Basket object and save it to the database
    # basket_item = Basket.objects.create(user=user, inventory_item=item)
    #
    # # Redirect the user to the basket page or any other appropriate page
    # return redirect('basket')







    # if request.method == 'POST':
    #     item_id = int(item_id)
    #     # Get the user's session
    #     session_key = request.session.session_key
    #     if not session_key:
    #         request.session.save()
    #         session_key = request.session.session_key
    #
    #     # Retrieve the list of item IDs from the session or create an empty list if it doesn't exist
    #     item_ids = request.session.get('basket_items', [])
    #     # Add the new item ID to the list
    #     if item_id not in item_ids:
    #         item_ids.append(item_id)
    #     # Save the updated list back to the session
    #     request.session['basket_items'] = item_ids
    #
    #     # Print the session data to the console for testing
    #     print("Basket items:")
    #     for id in item_ids:
    #         item = InventoryItem.objects.get(pk=id)
    #         print(f"ID: {item.id}, Name: {item.name}")
    #
    #     # Return a JSON response indicating success
    #     return JsonResponse({'message': 'Item added to basket successfully'})
    # else:
    #     # Return a JSON response indicating failure
    #     return JsonResponse({'error': 'Invalid request method'})


def get_basket(request):
    if request.method == 'GET':
        # Get the list of item IDs from the session
        item_ids = request.session.get('basket_items', [])
        # Retrieve the items from the database using the IDs
        borrowed_items = BorrowedItem.objects.all()
        # Create BorrowedItem instances for each item
        for item in borrowed_items:
            BorrowedItem.objects.create(user=request.user, item=item)
        # Clear the session
        request.session['basket_items'] = []
        # Render the basket page with the items
        return render(request, 'basket.html', {'items': borrowed_items})


def remove_item(request, item_id):
    # Retrieve the BasketItem object using the item_id
    basket_item = get_object_or_404(Basket, id=item_id)

    # Delete the BasketItem object from the database
    basket_item.delete()

    # Redirect to a success URL
    return redirect('basket')
