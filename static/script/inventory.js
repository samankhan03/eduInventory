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


document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all add-to-basket forms
    document.querySelectorAll('.add-to-basket-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            var itemId = form.getAttribute('data-item-id');

            var itemName = form.getAttribute('data-item-name');

            console.log('Item Name:', itemName);

            var formData = new FormData(form);
            formData.set('quantity', 1);

            fetch('/basket/add-to-basket/' + itemId + '/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Item [' + itemName + '] added to basket');
                    alert('Item [' + itemName + '] added to basket');
                } else {
                    alert('Failed to add item to basket');
                }
            })
            .catch(error => {
                alert('Network error:', error);
            });
        });
    });
});
