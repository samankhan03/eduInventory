document.getElementById('stock-filter').addEventListener('click', function() {
    var arrow = document.querySelector('.custom-dropdown .arrow');
    arrow.style.display = arrow.style.display === 'none' ? 'inline' : 'none';
});

function toggleDescription(product) {
    product.classList.toggle('active');
    console.log("active")}
