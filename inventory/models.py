from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        db_table = 'user'


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='Available')

    class Meta:
        db_table = 'inventory_item'


class BorrowedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    borrow_date = models.DateField()

    class Meta:
        db_table = 'borrowed_item'
