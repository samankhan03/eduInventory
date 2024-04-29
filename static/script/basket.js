document.querySelectorAll('.remove').forEach(button => {
    button.addEventListener('click', function() {
        const itemId = this.getAttribute('data-item-id');

        // Send AJAX request to remove the item
        fetch(`/remove-item/${itemId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}', // Include CSRF token
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Item removed successfully, update UI
                this.closest('.borrowed-item').remove();
            } else {
                // Handle error response
                console.error('Failed to remove item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


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

