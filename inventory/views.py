import datetime
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import FileResponse
from reportlab.pdfgen import canvas

from .models import *
from .forms import CreateUserForm


def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was created for " + form.cleaned_data['username'])

            return redirect('user-login')

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
    return render(request, 'dashboard_user.html', context)


def inventory_user(request):
    inventory_items = InventoryItem.objects.all()
    return render(request, 'inventory_user.html', {'inventory_items': inventory_items})


def login_page(request):
    return render(request, 'loginpage.html')


def dashboard_user(request):
    if request.user:
        basket_items = Basket.objects.all()
        historical_bookings = Reservation.objects.filter(user=request.user)
        current_reservations = Reservation.objects.filter(user=request.user)

        return render(request, 'dashboard_user.html',
                      {'basket': basket_items, 'historical_bookings': historical_bookings,
                       'current_reservations': current_reservations})
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

def admin_dashboard(request):
    return render(request, 'dashboard_admin.html')

def generate_inventory_pdf(request):
    response = FileResponse(generate_inventory_report(),
                            as_attachment=True,
                            filename='inventory_report.pdf')
    return response


def generate_inventory_report():
    from io import BytesIO
    from inventory.models import InventoryItem
    from reportlab.pdfgen import canvas

    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Creating the PDF document
        items = InventoryItem.objects.all()
        p.drawString(100, 800, "Inventory Report:")

        # Define the starting positions for each column
        x_positions = [100, 200, 300, 400, 500]  # Adjust as needed
        y = 750

        # Define the column width and height
        row_height = 15

        # Set the font size to be smaller


        for item in items:
            p.setFont("Helvetica", 8)  # Adjust the font name and size as needed
            # Draw item details in columns
            for attribute, position in zip(['name', 'location', 'onsite_only', 'quantity', 'availability'], x_positions):
                p.drawString(position, y, f"{attribute.capitalize()}: {getattr(item, attribute)}")
                y -= row_height

            # Add a horizontal line between items
            p.line(x_positions[0], y + 5, x_positions[-1], y + 5)
            y -= 15  # Adjust spacing between items

            # Check if the next item will fit in the remaining space
            if y < 50:
                # Add a new page
                p.showPage()
                # Reset y position for the new page
                y = 800

        p.save()

        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"Error generating inventory report: {e}")
        return None


def generate_usage_history_pdf(request):
    response = FileResponse(generate_usage_history_report(),
                            as_attachment=True,
                            filename='usage_history_report.pdf')
    return response


def generate_usage_history_report():
    from io import BytesIO
    from .models import BorrowedItem
    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Creating the PDF document
        p.drawString(100, 800, "Equipment Usage History Report:")

        # Define the starting positions for each column
        x_positions = [100, 200, 400]  # Adjust as needed
        y = 750

        # Define the column width and height
        column_width = 150
        row_height = 15

        # Fetch borrowed items from the database
        borrowed_items = BorrowedItem.objects.all()

        for borrowed_item in borrowed_items:
            p.setFont("Helvetica", 8)  # Adjust the font name and size as needed
            # Draw item details in columns
            for i, (attribute, position) in enumerate(zip(['user', 'item', 'borrow_date'], x_positions)):
                value = getattr(borrowed_item, attribute)
                if attribute == 'user':
                    value = value.username  # Assuming User has a username field
                elif attribute == 'item':
                    value = value.name  # Assuming InventoryItem has a name field
                p.drawString(position, y, f"{attribute.capitalize()}: {value}")
                y -= row_height

            # Add a horizontal line between items
            p.line(x_positions[0], y + 5, x_positions[-1] + column_width, y + 5)
            y -= 15  # Adjust spacing between items

            # Check if the next item will fit in the remaining space
            if y < 50:
                # Add a new page
                p.showPage()
                # Reset y position for the new page
                y = 800

        p.save()

        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"Error generating usage history report: {e}")
        return None

def generate_overdue_items_pdf(request):
    response = FileResponse(generate_overdue_items_report(),
                            as_attachment=True,
                            filename='overdue_items_report.pdf')
    return response
def generate_overdue_items_report():
    from io import BytesIO
    from inventory.models import InventoryItem
    from reportlab.pdfgen import canvas

    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Define the starting positions for each column
        x_positions = [100, 200, 300, 400, 500]  # Adjust as needed
        row_height = 15

        # Filter overdue items
        overdue_items = InventoryItem.objects.filter(return_date__lt=datetime.date.today())

        if overdue_items:
            p.drawString(100, 800, "Overdue Items Report:")

            for item in overdue_items:
                # Set the font size to be smaller
                p.setFont("Helvetica", 8)  # Adjust the font name and size as needed

                # Draw item details in columns
                y = 750  # Reset y coordinate for each item
                for attribute, position in zip(['name', 'item_type', 'status', 'quantity', 'availability'], x_positions):
                    p.drawString(position, y, f"{attribute.capitalize()}: {getattr(item, attribute)}")
                    y -= row_height

                # Add a horizontal line between items
                for i in range(len(x_positions) - 1):  # Draw lines between columns
                    p.line(x_positions[i], y + 5, x_positions[i + 1], y + 5)

                # Check if the next item will fit in the remaining space
                if y < 50:
                    # Add a new page
                    p.showPage()

        else:
            p.drawString(100, 800, "No Overdue Items Found.")

        p.save()

        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"Error generating overdue items report: {e}")
        return None


