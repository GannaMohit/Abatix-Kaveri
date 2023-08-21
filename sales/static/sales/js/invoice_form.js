function newRow(element, subform_name) {
  let form = document.getElementById(`${subform_name}_subform`);

  if (form.hidden) {
    form.hidden = false;
  }
}

function submitRow(element, table_name) {
  if (table_name == "products") {
    radioField = document.querySelector("#product_subform input[name='radio_type']:checked").value;
    table_name = radioField == "tagged" ? "products" : "untagged";
    subform_name = "products";
  }
  else {
    subform_name = table_name;
  }

  let tbody = document.querySelector(`#${table_name}_table tbody`);
  let tr = document.querySelector(`#${table_name}_table tbody tr:last-child`);
  let clone = tr.cloneNode(true);

  let changePrefixInputs = tr.querySelectorAll(`input[name^='${table_name}-__prefix__'], select[name^='${table_name}-__prefix__']`);
  changePrefixInputs.forEach( (input) => {
    let text = input.name;
    let result = text.replace("__prefix__", tr.rowIndex);
    input.setAttribute("name", result);
  });
  let total_forms = document.getElementById(`id_${table_name}-TOTAL_FORMS`);
  total_forms.value = parseInt(total_forms.value) + 1;

  tbody.appendChild(clone);
  tr.id = "selected";
  tr.querySelector(".cross").style.display = "inline";


  updateValues(table_name, subform_name);
  let form = document.getElementById(`${subform_name}_subform`);

  form.reset();

  selected = document.querySelector(`#${table_name}_table #selected`);
  selected.id = "";
}


function updateValues(table_name, subform_name) {
  let source = document.querySelectorAll(`#${subform_name}_subform input, #${subform_name}_subform select`);
  source_split_func = (element) => [element.name];
  dest_split_func = (element) => element.name.split("-");


  for (let i = 0; i < source.length; i++) {
    let source_names = source_split_func(source[i]);
    let source_name = source_names[source_names.length - 1];
    let dest = document.querySelector(`#${table_name}_table #selected [name$=-${source_name}]`);
    let cell_value = document.querySelector(`#${table_name}_table #selected #id_${source_name}_table`);
  
    if (dest != null) {
      dest.value = source[i].value;
    }

    if (cell_value != null) {
      if (source[i].tagName == "SELECT") {
        cell_value.innerText = source[i].selectedOptions[0].text;
      }
      else {
        cell_value.innerText = source[i].value;
      }
    }
  }
  // calculateTotals();
}

function deleteRow(element) {
  let tr = element.parentElement.parentElement;
  // TODO: Add logic to add Form-#-Delete to POST data
  let delete_field = tr.querySelector("input[name$='-DELETE']");
  delete_field.checked = true;
  tr.style.display = "none";
}

function switchProductFields(element) {
  fields = ['metal', 'type', 'purity', 'category', 'pieces', 'gross_weight', 'less_weight', 'studs_weight', 'net_weight'];

  fieldHandler = (field, boolean) => {field.disabled = boolean; field.value = "";}

  if (element.value == "tagged") {
    fieldHandler(document.querySelector("#product_subform #id_product"), false);

    fields.forEach(field => fieldHandler(document.querySelector(`#product_subform #id_${field}`), true));
  }
  else {
    fieldHandler(document.querySelector("#product_subform #id_product"), true);

    fields.forEach(field => fieldHandler(document.querySelector(`#product_subform #id_${field}`), false));
  }
}

function displayFields() {
  let method = document.querySelector("#payment_subform_div #id_method");
  let method_value = method.value;
  let form = document.querySelector('#payments_subform');
  form.reset();
  method.value = method_value

  let payment_divs = document.querySelectorAll('#payment_subform_div div');

  function hide_div_func (e, display) {
    e.style.display = display;
  }

  payment_divs.forEach( (div) => hide_div_func(div, 'none'));

  let method_div = method.parentElement;
  let date_div = document.querySelector("#payment_subform_div #id_date").parentElement;
  let name_div = document.querySelector("#payment_subform_div #id_name").parentElement;
  let amount_div = document.querySelector("#payment_subform_div #id_amount").parentElement;

  hide_div_func(method_div, 'inline-flex');
  hide_div_func(date_div, 'inline-flex');
  hide_div_func(name_div, 'inline-flex');
  hide_div_func(amount_div, 'inline-flex');

  switch(method.value) {
    case "Cash": {
      break;
    }
    case "Credit Card":
    case "Debit Card": {
      let card_inputs = document.querySelectorAll("#payment_subform_div input[id^='id_card_']");
      for (let i = 0; i < card_inputs.length; i++) {
        card_inputs[i].parentElement.style.display = "inline-flex";
      }
      break;
    }
    case "Cheque": {
      let cheque_inputs = document.querySelectorAll("#payment_subform_div input[id^='id_cheque_']");
      for (let i = 0; i < cheque_inputs.length; i++) {
        cheque_inputs[i].parentElement.style.display = "inline-flex";
      }
      break;
    }
    case "IMPS":
    case "NEFT":
    case "RTGS": {
      let wire_inputs = document.querySelectorAll("#payment_subform_div input[id^='id_wire_']");
      for (let i = 0; i < wire_inputs.length; i++) {
        wire_inputs[i].parentElement.style.display = "inline-flex";
      }
      break;
    }
    case "UPI": {
      let upi_inputs = document.querySelectorAll("#payment_subform_div input[id^='id_upi_']");
      for (let i = 0; i < upi_inputs.length; i++) {
        upi_inputs[i].parentElement.style.display = "inline-flex";
      }
      break;
    }
    default: {}
  }
}

window.onload = () => {
  let method = document.querySelector("#payment_subform_div #id_method");
  method.oninput = displayFields;
}

function validateFunction(element, url, string, field) {
  let subform_name = `${string}s`;
  element.setCustomValidity("");
  element.reportValidity();
  let inputs = document.querySelectorAll(`#${subform_name}_table [name$='-product']`);
  let deletes = document.querySelectorAll(`#${subform_name}_table [name$='-DELETE']`);
  let count = 0;
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].value == element.value && Boolean(deletes[i].value) == false) {
      element.setCustomValidity(`The ${string} is already selected above.`);
      element.reportValidity();
      return;
    }
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
      element.setCustomValidity(`This ${string} does not exist.`);
      element.reportValidity();
    }
    else if (product[field]) {
      element.setCustomValidity(`The ${string} is already used.`)
      element.reportValidity();
      return;
    }
    else {
      element.setCustomValidity("");
      let source = product;
      dest = document.querySelectorAll(`#${subform_name}_subform input, #${subform_name}_subform select`);
      for (const source_name in source) {
        for (let j = 0; j < dest.length; j++) {
          let dest_name = dest[j].name;
          if (source_name == dest_name) {
            dest[j].value = source[source_name];
            break;
          }
        }
      }
    }
  });
}

function validateProductID(element, url) {
  validateFunction(element, url, "product", 'sold');
}

function validateAdvanceID(form, url) {
  let element = form.querySelector("#id_advance");

  validateFunction(element, url, "advance", 'redeemed');
}


// TODO: calculateTax()
// TODO: calculateTotals()


