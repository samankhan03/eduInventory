from django.contrib import admin
from .models import User, InventoryItem, BorrowedItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass  # You can customize the admin interface for User if needed


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    pass  # You can customize the admin interface for InventoryItem if needed


@admin.register(BorrowedItem)
class BorrowedItemAdmin(admin.ModelAdmin):
    pass  # You can customize the admin interface for BorrowedItem if needed
