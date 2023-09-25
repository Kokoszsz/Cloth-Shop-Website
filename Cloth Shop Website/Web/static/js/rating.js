const stars = document.querySelectorAll('.rating input');
const ratingValue = document.getElementById('rating-value');
const resetBtn = document.getElementById('reset-btn');

stars.forEach((star) =>
star.addEventListener('click', () => {
  const rating = star.value;
  const productId = star.closest('.rating').dataset.productId; // Retrieve the product ID from the data attribute

  // Create a data object to send as JSON
  const data = { rating: rating, productId: productId };

  // Send the rating and product ID to Flask app 
  fetch('/save_rating', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('User rated: ' + rating + ' for product ID: ' + productId);
    })
    .catch((error) => {
      console.error('Error sending rating:', error);
    });
})
);

if (resetBtn) {
  resetBtn.addEventListener('click', () => {
      
      stars.forEach((star) => (star.checked = false));
      
      const productId = resetBtn.closest('.rating').dataset.productId;
      const data = {productId: productId};
      // Send the rating and product ID to Flask app
      fetch('/reset_rating', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      })
      .then((response) => response.json())
      console.log('Rating reset.');
  });
}