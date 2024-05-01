// Author: Tilly Richter
// Co-Author: Yhuen Yutico


// Function for removing items in basket
document.querySelectorAll('.remove').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.getAttribute('data-item-id');

        fetch(`/remove-item/${itemId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                this.closest('.borrowed-item').remove();
            } else {
                console.error('Failed to remove item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


// Funtion for reserving items in basket
document.addEventListener('DOMContentLoaded', function() {
    const reserveButton = document.querySelector('.reserve');
    reserveButton.addEventListener('click', function() {
         const formData = new FormData();
        fetch(`/reserve-all-items/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            alert('All items reserved successfully');
        })
        .catch(error => console.error('Error:', error));
    });
});

