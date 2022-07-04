function validateID(element, url) {
  element.setCustomValidity("");
  element.reportValidity();
  let data = { "id": element.value.toString() };
  fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
  .then(response => response.json())
  .then(function(product) {
    if (product['sold'] === 1) {
      element.setCustomValidity("The product is already sold.");
      element.reportValidity();
      return;
    }
    else {
      element.setCustomValidity("");
    }
  });
}
