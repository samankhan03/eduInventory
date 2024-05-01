# Author: Yhuen Yutico
# Co-Author: Tilly Richter
from django.contrib import admin
from .models import InventoryItem, BorrowedItem, Reservation, Basket


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'status', 'quantity', 'availability')
    list_filter = ('item_type', 'status', 'availability')
    search_fields = ('name', 'item_type', 'comments')
    list_per_page = 50


@admin.register(BorrowedItem)
class BorrowedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_name', 'borrow_date', 'get_return_date')
    list_filter = ('borrow_date', 'user__username', 'item__name')
    search_fields = ('user__username', 'item__name')
    list_per_page = 50

    def get_return_date(self, obj):
        return obj.item.return_date

    def get_item_name(self, obj):
        return obj.item.name

    get_return_date.short_description = 'Return Date'
    get_item_name.short_description = 'Item Name'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'inventory_item_name', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'inventory_item__name')
    list_per_page = 50

    def inventory_item_name(self, obj):
        return obj.inventory_item.name

    inventory_item_name.short_description = 'Inventory Item Name'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_name', 'reservation_date', 'get_return_date', 'status')
    list_filter = ('status', 'reservation_date', 'return_date')
    search_fields = ('user__username', 'inventory_item__name')
    list_per_page = 50

    def get_item_name(self, obj):
        return obj.item.name

    def get_return_date(self, obj):
        return obj.item.return_date

    get_item_name.short_description = 'Item Name'
    get_return_date.short_description = 'Return Date'
