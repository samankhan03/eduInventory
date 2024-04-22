# management/commands/populate_inventory.py

import os
import pandas as pd
import django
from django.core.management.base import BaseCommand
from inventory.models import InventoryItem

settings_module = 'settings.py'
django.setup()


class Command(BaseCommand):
    help = 'Populates the InventoryItem table from an Excel file'

    def handle(self, *args, **kwargs):
        excel_file_path = os.path.join('media', 'equipment.xlsx')  # Path to your Excel file
        excel_data = pd.read_excel(excel_file_path)
        for index, row in excel_data.iterrows():
            name = row['Device Name']
            item_type = row['Device Type']
            quantity = row['Quantity']
            audit_date = row['Audit']
            location = row['Location']
            status = row['Status']
            comments = row['Comments']
            availability = True if str(status) == "nan" or status.lower() == "available" else False
            # Create InventoryItem objects and save them to the database
            InventoryItem.objects.create(
                name=name,
                item_type=item_type,
                status=status,
                quantity=quantity,
                availability=availability,
                location=location,
                audit_date=audit_date,
                comments=comments)

        self.stdout.write(self.style.SUCCESS('Inventory items populated successfully'))
