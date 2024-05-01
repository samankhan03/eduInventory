// Author: Tilly Richter
// Co-Author: Yhuen Yutico

// function to toggle mini page when button is clicked
var buttons = document.querySelectorAll('.show-info-button');

buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        toggleMiniPage(this); // Call toggleMiniPage function when the button is clicked
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.cards');

    cards.forEach(function(card) {
        card.addEventListener('click', function() {
            var miniPage = this.querySelector('.mini-page');
            if (miniPage.classList.contains('visible')) {
                miniPage.classList.remove('visible');
            } else {
                miniPage.classList.add('visible');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all add-to-basket forms
    document.querySelectorAll('.rebook-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            var itemId = form.getAttribute('data-item-id');

            var itemName = form.getAttribute('data-item-name');

            console.log('Item Name:', itemName);
            console.log('Item Id: ', itemId);

            var formData = new FormData(form);
            formData.set('quantity', 1);

            fetch('/add-to-basket/' + itemId + '/', {
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