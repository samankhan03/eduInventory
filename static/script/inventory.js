function filterInventory() {
    let selectedAvailability = document.getElementById("stock-filter").value;
    let selectedType = document.getElementById("type-filter").value;

    let inventoryItems = document.querySelectorAll(".inventory-item");
    inventoryItems.forEach(function(item) {
        let availability = item.dataset.availability;
        let type = item.dataset.itemtype;
        let availabilityString = availability === 'True' ? 'Available' : 'Unavailable';
        let showItem = (selectedAvailability === 'all' || selectedAvailability === availabilityString) &&
                       (selectedType === 'all' || selectedType === type);

        if (showItem) {
            item.style.display = 'table-row';
        } else {
            item.style.display = 'none';
        }
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.querySelector(".search-bar form");
    const searchInput = document.querySelector(".search-bar input[type='text']");

    searchForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const query = searchInput.value.toLowerCase().trim();
        filterBySearch(query);
    });

    function filterBySearch(query) {
        const inventoryItems = document.querySelectorAll(".inventory-item");

        inventoryItems.forEach(function(item) {
            const itemName = item.querySelector("td:first-child").textContent.toLowerCase();
            if (itemName.includes(query)) {
                item.style.display = "table-row";
            } else {
                item.style.display = "none";
            }
        });
    }
});