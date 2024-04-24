from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
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
    return render(request, 'dashboard_user.html')


def basket(request):
    basket_items = Basket.objects.all()
    return render(request, 'basket.html', {'basket': basket_items})


def admin(request):
    return HttpResponse('<p>hello </p>')


def add_item(request, item_id):
    if request.method == 'POST':
        item_id = int(item_id)
        basket_item = Basket.objects.filter(user=request.user, inventory_item_id=item_id).first()

        if basket_item:
            basket_item.quantity += 1
            basket_item.save()
        else:
            inventory_item = get_object_or_404(InventoryItem, pk=item_id)
            basket_item = Basket.objects.create(user=request.user, inventory_item=inventory_item, quantity=1)
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
