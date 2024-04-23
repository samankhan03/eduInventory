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
            // Prevent the default form submission behavior
            event.preventDefault();

            // Get the item ID from the form's data attribute
            var itemId = form.getAttribute('data-item-id');

            // Create a new FormData object to send the form data
            var formData = new FormData(form);

            // Send the AJAX request to add the item to the basket
            fetch('/basket/add-to-basket/' + itemId + '/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    // Optionally, display a success message to the user
                    console.log('Item added to basket successfully');
                } else {
                    // Handle the error response
                    console.error('Failed to add item to basket');
                }
            })
            .catch(error => {
                // Handle any network errors
                console.error('Network error:', error);
            });
        });
    });
});
