const stars = document.querySelectorAll('.rating input');
const ratingValue = document.getElementById('rating-value');
const resetBtn = document.getElementById('reset-btn');

stars.forEach((star) =>
star.addEventListener('click', () => {
  const rating = Number(star.value);
  const productId = star.closest('.rating').dataset.productId; // Retrieve the product ID from the data attribute

  fetch(`/api/v1/products/${productId}/rating`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ rating: rating }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`status ${response.status}`);
      }
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
      fetch(`/api/v1/products/${productId}/rating`, {
          method: 'DELETE',
      })
      .then((response) => {
          if (response.status === 204) {
              console.log('Rating reset.');
          }
      })
      .catch((error) => {
          console.error('Error resetting rating:', error);
      });
  });
}
