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
        // Select the add to cart forms
        const addToCartForms = document.querySelectorAll('.add-to-cart-form');

        // Add event listeners to each form
        addToCartForms.forEach(form => {
            form.addEventListener('submit', async function(event) {
                event.preventDefault(); // Prevent the default form submission

                // Get the form data
                const formData = new FormData(form);
                try {
                    // Send a POST request to the add-item endpoint
                    const response = await fetch(form.action, {
                        method: 'POST',
                        body: formData
                    });

                    // Parse the JSON response
                    const data = await response.json();

                    // Check if the item was added successfully
                    if (data.success) {
                        // Show a success message to the user
                        alert('Item added to cart successfully!');
                    } else {
                        // Show an error message if something went wrong
                        alert('Failed to add item to cart. Please try again later.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred while processing your request. Please try again later.');
                }
            });
        });

});
