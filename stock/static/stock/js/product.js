function validateID(element, url) {
  element.setCustomValidity("");
  element.reportValidity();
  let csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
  let data = { "id": element.value.toString() };
  let headers = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify(data)
  }
  fetch(url, headers)
  .then(response => response.json())
  .then(function(product) {
    if (Object.keys(product).length === 0) {
      element.setCustomValidity("The product does not exist.");
      element.reportValidity();
      return;
    }
    if (product['sold']) {
      element.setCustomValidity("The product is already sold.");
      element.reportValidity();
    }
    else {
      element.setCustomValidity("");
    }
  });
}
