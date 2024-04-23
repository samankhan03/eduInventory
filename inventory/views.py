from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    return render(request, 'dashboard_user.html')


def basket(request):
    inventory_items = InventoryItem.objects.all()
    return render(request, 'basket.html', {'inventory_items': inventory_items})


def admin(request):
    return HttpResponse('<p>hello </p>')
