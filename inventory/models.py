from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='Available')
    quantity = models.IntegerField(default=0)
    audit_date = models.DateField(default=None, null=True, blank=True)
    location = models.CharField(max_length=100, default='')
    availability = models.BooleanField(default=False)
    comments = models.CharField(max_length=200, default='')
    onsite_only = models.BooleanField(default=False)
    return_date = models.DateField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'inventory_item'


class BorrowedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'borrowed_item'


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    reservation_date = models.DateField(default=None, null=True, blank=True)
    return_date = models.DateField(default=None, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'reservation'
