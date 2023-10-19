document.addEventListener('DOMContentLoaded', function() {
  document.body.addEventListener('click', function(e) {
    var link = e.target.closest('.add-to-basket');
    if (link) {
      e.preventDefault();
      var productID = link.getAttribute('data-product_id');

      var modal = document.getElementById("myModal");
      modal.style.display = "block";
      document.body.style.overflow = 'hidden';

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/add-to-basket");
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.send(JSON.stringify({ product_ID: productID }));
    }
  });
});







function closeModal() {
  var modal = document.getElementById("myModal");

  document.body.style.overflow = 'auto';
  modal.style.display = "none";
}
