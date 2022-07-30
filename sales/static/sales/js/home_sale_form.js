function addRow(element) {
  let selected = document.getElementById('selected-1');
  if (selected !== null) {
    selected.id = "";
  }
  element.parentElement.parentElement.id = "selected-1";
  if (element.id === "id_products-__prefix__-product") {
    let tbody = element.parentElement.parentElement.parentElement;
    let clone = element.parentElement.parentElement.cloneNode(true);
    let changePrefixInputs = element.parentElement.querySelectorAll("input[name^='products-__prefix__']");
    changePrefixInputs.forEach( (input) => {
      let text = input.name;
      let result = text.replace("__prefix__", element.parentElement.parentElement.rowIndex);
      input.setAttribute("name", result);
    });
    let total_forms = document.getElementById("id_products-TOTAL_FORMS");
    total_forms.value = parseInt(total_forms.value) + 1;
    tbody.appendChild(clone);
  }
  element.id = "";
  element.placeholder = "";
  element.parentElement.parentElement.lastElementChild.children[0].hidden = false;
}

function validateID(element, url) {
  let tds = element.parentElement.parentElement.children;
  tds[1].innerHTML = "";
  tds[2].innerHTML = "";
  tds[3].innerHTML = "";
  tds[4].innerHTML = "";
  tds[5].innerHTML = "";
  tds[6].innerHTML = "";
  tds[7].innerHTML = "";
  tds[8].innerHTML = "";
  tds[9].innerHTML = "";
  element.setCustomValidity("");
  element.reportValidity();
  let inputs = document.querySelectorAll("input[name$='-product']");
  let count = 0;
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].value === element.value) {
      count = count + 1;
    }
  }

  if (count > 1) {
    element.setCustomValidity("The product is already selected above.");
    element.reportValidity();
    return;
  }

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
    }
    else if (product['sold']) {
      element.setCustomValidity("The product is already sold.");
      element.reportValidity();
      return;
    }
    else {
      element.setCustomValidity("");
      tds[1].innerHTML = product['metal'];
      tds[2].innerHTML = product['purity'];
      tds[3].innerHTML = product['category'];
      tds[4].innerHTML = product['description'];
      tds[5].innerHTML = product['pieces'];
      tds[6].innerHTML = product['gross_weight'] + " g";
      tds[7].innerHTML = product['less_weight'] + " g";
      tds[8].innerHTML = product['net_weight'] + " g";
      tds[9].innerHTML = product['register_id'];
      calculateTotals();
    }
  });
}

document.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    let add = document.getElementById('id_products-__prefix__-product');
    add.focus();
  }
});

function deleteRow(element) {
  element.parentElement.parentElement.style.display = "none";
  calculateTotals()
  let selected = document.getElementById('selected-1');
  if (selected !== null) {
    selected.id = "";
  }
  // TODO: Write logic to add the form in FORM-#-DELETE
}

function calculateTotals() {
  let pcsTotal = document.getElementById('pcsTotal');
  let gwTotal = document.getElementById('gwTotal');
  let lwTotal = document.getElementById('lwTotal');
  let nwTotal = document.getElementById('nwTotal');
  let trs = document.getElementById('table').children[0].children;
  let temp1 = 0;
  let temp2 = 0.0;
  let temp3 = 0.0;
  let temp4 = 0.0;
  for (let i = 0; i < trs.length; ++i) {
    if (!trs[i].style.diplay){
      temp1 += Number(trs[i].children[5].innerHTML);
      temp2 += Number(trs[i].children[6].innerHTML.substring(0, trs[i].children[6].innerHTML.length - 2));
      temp3 += Number(trs[i].children[7].innerHTML.substring(0, trs[i].children[7].innerHTML.length - 2));
      temp4 += Number(trs[i].children[8].innerHTML.substring(0, trs[i].children[8].innerHTML.length - 2));
    }
  }
  pcsTotal.innerHTML = temp1.toLocaleString();
  gwTotal.innerHTML = temp2.toLocaleString() + " g";
  lwTotal.innerHTML = temp3.toLocaleString() + " g";
  nwTotal.innerHTML = temp4.toLocaleString() + " g";
}
