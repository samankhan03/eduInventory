function hideCard(cardId, action) {
        var card = document.getElementById(cardId);
        if (card) {
            card.style.display = "none";
            var message;
            var color;
            if (action === "approve") {
                message = "User has been approved";
                color = "#7cb46b"; // Set color to green for approval
            } else if (action === "deny") {
                message = "User has been denied";
                color = "#F5554A"; // Set color to red for denial
            }
            var messageElement = document.createElement("div");
            messageElement.innerHTML = message;
            messageElement.style.color = color; // Apply color style
            card.parentNode.insertBefore(messageElement, card.nextSibling);

            setTimeout(function() {
                messageElement.remove();
            }, 3000); // Timer before message disappears
        }
    }