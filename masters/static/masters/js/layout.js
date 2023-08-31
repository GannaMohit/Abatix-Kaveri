function newRow(element, subform_name) {
    let form = document.getElementById(`${subform_name}_subform`);

    if (form.hidden) {
        form.hidden = false;
    }
}

function submitRow(element, table_name, subform_name) {
  let tbody = document.querySelector(`#${table_name}_table tbody`);
  let tr = document.querySelector(`#${table_name}_table tbody tr:last-child`);
  let clone = tr.cloneNode(true);

  let changePrefixInputs = tr.querySelectorAll(`input[name^='${table_name}-__prefix__'], select[name^='${table_name}-__prefix__']`);
  changePrefixInputs.forEach( (input) => {
    let text = input.name;
    let result = text.replace("__prefix__", tr.rowIndex - 1);
    input.setAttribute("name", result);
  });
  let total_forms = document.getElementById(`id_${table_name}-TOTAL_FORMS`);
  total_forms.value = parseInt(total_forms.value) + 1;

  tbody.appendChild(clone);
  tr.id = "selected";
  tr.style.display = "";
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
        else if (source[i].type == "checkbox"){
          cell_value.innerText = source[i].checked ? "Yes" : "No";
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
    let delete_field = tr.querySelector("input[name$='-DELETE']");
    delete_field.checked = true;
    tr.style.display = "none";
}

function validateFunction(element, url, string, field) {
    let subform_name = `${string}s`;
    element.setCustomValidity("");
    element.reportValidity();
    let inputs = document.querySelectorAll(`#${subform_name}_table [name$='-${string}']`);
    let count = 0;
    for (let i = 0; i < inputs.length; i++) {
      if (inputs[i].value == element.value && inputs[i].parentElement.parentElement.parentElement.style.display != "none") {
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
        element.setCustomValidity(`The ${string} is already sold.`)
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

function calulateTotal(inputs, deletes) {
  let val = 0;
  for (let i = 0; i < inputs.length; ++i) {
    if (inputs[i].innerText != '') {
      if (Boolean(deletes[i].checked) == false) {
        val += Number(inputs[i].innerText);
      }
    }
  }
  return val;
}

function setSerialNumber(table_name) {
  let trs = document.querySelectorAll(`#${table_name}_table tbody tr`);
  for (let i = 0; i < trs.length -1; i++) {
    const tr = trs[i];
    let serial_number = tr.querySelector("#id_serial_number_table");
    serial_number.innerText = i+1;
  }
}

function calculateNetWeight() {
  let gw = document.getElementById('id_gross_weight');
  let lw = document.getElementById('id_less_weight');
  let nw = document.getElementById('id_net_weight');

  nw.value = Number(gw.value - lw.value).toFixed(3) 
}

function calculateTax() {
  let subtotal = document.querySelector(`#id_subtotal`);
  let sgst = document.querySelector(`#id_sgst`);
  let cgst = document.querySelector(`#id_cgst`);
  let igst = document.querySelector(`#id_igst`);
  let tcs = document.querySelector(`#id_tcs`);
  let total = document.querySelector(`#id_total`);
  let state = document.querySelector('#id_state');

  let csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
  let headers = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    }
  }
  fetch('/masters/_fetch_taxes', headers)
  .then(response => response.json())
  .then(function(tax_ajax) {
    tax = tax_ajax.tax;
    if (state.value == 27) {
      sgst.value = Number(tax.find(t => t['fields']["type"] == 'sgst')["fields"]["percentage"] * subtotal.value / 100).toFixed(0);
      cgst.value = Number(tax.find(t => t['fields']["type"] == 'cgst')["fields"]["percentage"] * subtotal.value / 100).toFixed(0);
      igst.value = 0;
      tcs.value = 0;
    }
    else {
      sgst.value = 0;
      cgst.value = 0;
      igst.value = Number(tax.find(t => t['fields']["type"] == 'igst')["fields"]["percentage"] * subtotal.value / 100).toFixed(0);
      tcs.value = 0;
    }
    total.value = Number(Number(subtotal.value) + Number(cgst.value) + Number(sgst.value) + Number(igst.value)).toFixed(0);
  });
}

function fetchCustomer() {
  let cust = document.querySelector("#customer_box #id_contact");
  let csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
  let data = { "contact": cust.value.toString() };
  let headers = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify(data)
  }
  fetch('/masters/_fetch_customer', headers)
  .then(response => response.json())
  .then(function(customer) {
    if (Object.keys(customer).length != 0) {
      let source = customer;
      dest = document.querySelectorAll(`#customer_box input, #customer_box select, #customer_box textarea`);
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

function disbaleEnter() {
  document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
    }
  }); 
}