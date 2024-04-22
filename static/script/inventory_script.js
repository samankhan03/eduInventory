
document.getElementById('stock-filter').addEventListener('change', function() {
    filterInventory(); // Call the filterInventory function when the selection changes
});

function filterInventory() {
    let selectedAvailability = document.getElementById("stock-filter").value;
    let selectedType = document.getElementById("type-filter").value;

    let inventoryItems = document.querySelectorAll(".inventory-item");
    console.log(selectedAvailability);
    inventoryItems.forEach(function(item) {
        let availability = item.dataset.availability;
        let type = item.dataset.itemtype;
        let availabilityString = availability === 'True' ? 'Available' : 'Unavailable';

        let showItem = (selectedAvailability === 'all' || selectedAvailability === availabilityString) &&
                       (selectedType === 'all' || " " + selectedType === type);

        if (showItem) {
            item.style.display = 'table-row';
        } else {
            item.style.display = 'none';
        }
    });

}




