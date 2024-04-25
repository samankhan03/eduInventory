from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    user = request.user
    user_profile = User.objects.get(user=user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'dashboard.html', context)


def inventory_user(request):
    inventory_items = InventoryItem.objects.all()
    return render(request, 'inventory_user.html', {'inventory_items': inventory_items})


def login_page(request):
    return render(request, 'loginpage.html')


def dashboard_user(request):
    if request.user:
        basket_items = Basket.objects.all()
        return render(request, 'dashboard_user.html', {'basket': basket_items})
    else:
        return redirect('inventory-user')


def basket(request):
    basket_items = Basket.objects.all()
    return render(request, 'basket.html', {'basket': basket_items})


def add_item(request, item_id):
    if request.method == 'POST':
        item_id = int(item_id)
        basket_item = Basket.objects.filter(user=request.user, inventory_item_id=item_id).first()

        if basket_item:
            basket_item.quantity += 1
            basket_item.save()
        else:
            inventory_item = get_object_or_404(InventoryItem, pk=item_id)
            Basket.objects.create(user=request.user, inventory_item=inventory_item, quantity=1)

        return JsonResponse({'message': 'Item added to basket successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def get_basket(request):
    if request.method == 'GET':
        borrowed_items = BorrowedItem.objects.all()
        for item in borrowed_items:
            BorrowedItem.objects.create(user=request.user, item=item)
        request.session['basket_items'] = []
        return render(request, 'basket.html', {'items': borrowed_items})


def remove_item(request, item_id):
    basket_item = get_object_or_404(Basket, id=item_id)
    basket_item.delete()
    return redirect('basket')


def reserve_all_items(request):
    if request.method == 'POST':
        basket_items = Basket.objects.filter(user=request.user)
        for basket_item in basket_items:
            inventory_item = basket_item.inventory_item
            inventory_item.availability = False
            inventory_item.save()
            inventory_item.return_date = timezone.now() + timedelta(days=7)
            inventory_item.save()
            BorrowedItem.objects.create(user=request.user, item=inventory_item)
            reservation = Reservation.objects.create(user=request.user, item=inventory_item)
            reservation.reservation_date = timezone.now()
            reservation.return_date = timezone.now() + timedelta(days=7)
            reservation.save()
            inventory_item.quantity -= basket_item.quantity
            if inventory_item.quantity <= 0:
                inventory_item.quantity = 0
            inventory_item.save()

            basket_item.delete()

        return redirect('basket')
    else:
        return JsonResponse({'error': 'Invalid request method'})

def logout_view(request):
    logout(request)
    return redirect('user-login')
