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
// document.addEventListener('DOMContentLoaded', function() {
//     var myCard = document.getElementById('myCard');
//
//     myCard.addEventListener('click', function() {
//         // Your card click functionality goes here
//         var miniPage = this.querySelector('.mini-page');
//         if (miniPage.classList.contains('visible')) {
//             miniPage.classList.remove('visible');
//         } else {
//             miniPage.classList.add('visible');
//         }
//     });
// });