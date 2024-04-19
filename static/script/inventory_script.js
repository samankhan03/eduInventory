document.getElementById('stock-filter').addEventListener('click', function() {
    var arrow = document.querySelector('.custom-dropdown .arrow');
    arrow.style.display = arrow.style.display === 'none' ? 'inline' : 'none';
});

function toggleDescription(product) {
    product.classList.toggle('active');
    console.log("active")}


function filterInventory() {
    let selectedValue = document.getElementById("stock-filter").value;
    let inventoryItems = document.querySelectorAll(".inventory-item");

    inventoryItems.forEach(function(item) {
        let status = item.dataset.status;
        if (selectedValue === 'all' || selectedValue === status) {
            item.style.display = 'table-row';
        } else {
            item.style.display = 'none';
        }
    });
}
