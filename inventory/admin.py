from django.contrib import admin
from .models import User, InventoryItem, BorrowedItem



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'status', 'quantity', 'availability')
    list_filter = ('item_type', 'status', 'availability')
    search_fields = ('name', 'item_type', 'comments')


@admin.register(BorrowedItem)
class BorrowedItemAdmin(admin.ModelAdmin):
    pass
