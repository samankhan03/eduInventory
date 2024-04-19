# management/commands/populate_inventory.py

import os
import pandas as pd
import django
from django.core.management.base import BaseCommand
from inventory.models import InventoryItem

# Configure Django settings (replace 'your_project.settings' with the actual path to your settings module)
settings_module = 'settings.py'
django.setup()


class Command(BaseCommand):
    help = 'Populates the InventoryItem table from an Excel file'

    def handle(self, *args, **kwargs):
        excel_file_path = os.path.join('media', 'equipment.xlsx')  # Path to your Excel file
        excel_data = pd.read_excel(excel_file_path)

        # Select only the "Device Name", "Device Type" and "Status" columns
        excel_data = excel_data[['Device Name', 'Device Type', 'Status']]

        # Iterate over rows in the DataFrame and create InventoryItem objects
        for index, row in excel_data.iterrows():
            name = row['Device Name']
            device_type = row['Device Type']
            status = row['Status']
            print(f'{status}   {type(status)}  ==  {str(status)} ')
            if str(status) == "nan" or status == "available" or status == "Available":
                status = "Available"
            else:
                status = "Unavailable"

            # Create InventoryItem objects and save them to the database
            InventoryItem.objects.create(name=name, device_type=device_type, status=status)

        self.stdout.write(self.style.SUCCESS('Inventory items populated successfully'))
