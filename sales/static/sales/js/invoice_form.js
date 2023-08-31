function newProductRow(element) {
  newRow(element, 'products');
}

function newAdvanceRow(element) {
  newRow(element, 'advances');
}

function newPaymentRow(element) {
  newRow(element, 'payments');
  displayFields()
}

function submitProductRow(element) {
  radioField = document.querySelector("#product_subform input[name='radio_type']:checked").value;
  table_name = radioField == "tagged" ? "products" : "untagged";
  subform_name = "products";

  submitRow(element, table_name, subform_name);
  calculateTaxTable();
  calulateTotals();
}

function submitAdvanceRow(element) {
  submitRow(element, 'advances', 'advances');
}

function submitPaymentRow(element) {
  submitRow(element, 'payments', 'payments');
  setSerialNumber('payments');
}

function deleteProductRow(element) {
  deleteRow(element);
  calulateTotals();
}

function switchProductFields(element) {
  fields = ['metal', 'type', 'purity', 'category', 'pieces', 'gross_weight', 'less_weight', 'studs_weight'];

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

function calculateTaxTable() {
  let tax_tables = document.querySelectorAll('.products_table #id_tax_table');
  let tax_inputs = document.querySelectorAll(`.products_table [name$='-tax']`);
  let sgst_inputs = document.querySelectorAll(`.products_table [name$='-sgst']`);
  let cgst_inputs = document.querySelectorAll(`.products_table [name$='-cgst']`);
  let igst_inputs = document.querySelectorAll(`.products_table [name$='-igst']`);

  for (let i = 0; i < tax_inputs.length - 1; i++) {
    if (sgst_inputs[i].value != '') {
      tax_tables[i].innerText = Number(Number(sgst_inputs[i].value)+Number(cgst_inputs[i].value)+Number(igst_inputs[i].value)).toFixed(0);
      tax_inputs[i].value = Number(Number(sgst_inputs[i].value)+Number(cgst_inputs[i].value)+Number(igst_inputs[i].value)).toFixed(0);
    }
  }
}

function validateProductID(element) {
  validateFunction(element, '/stock/_fetch_product', "product", 'sold');
}

function validateAdvanceID(form) {
  let element = form.querySelector("#id_advance");

  validateFunction(element, '/sales/_fetch_advance', "advance", 'redeemed');
}

function calulateTotals() {
  let net_weight_inputs = document.querySelectorAll(`.products_table #id_net_weight_table`);
  let subtotal_inputs = document.querySelectorAll(`.products_table #id_subtotal_table`);
  let tax_inputs = document.querySelectorAll(`.products_table #id_tax_table`);
  let total_inputs = document.querySelectorAll(`.products_table #id_total_table`);
  let delete_inputs = document.querySelectorAll(`.products_table [name$='-DELETE']`);

  let nw = document.getElementById('id_net_weight_total');
  let sub = document.getElementById('id_subtotal_total');
  let tax = document.getElementById('id_tax_total');
  let tot = document.getElementById('id_total_total');
  nw.innerText = `${Number(calulateTotal(net_weight_inputs, delete_inputs)).toFixed(3)} g`;
  sub.innerText = `₹${Number(calulateTotal(subtotal_inputs, delete_inputs)).toFixed(2)}`;
  tax.innerText = `₹${Number(calulateTotal(tax_inputs, delete_inputs)).toFixed(2)}`;
  tot.innerText = `₹${Number(calulateTotal(total_inputs, delete_inputs)).toFixed(2)}`;
}

window.onload = () => {
  disbaleEnter();
  let method = document.querySelector("#payment_subform_div #id_method");
  let gw = document.getElementById('id_gross_weight');
  let lw = document.getElementById('id_less_weight');
  let subtotal = document.querySelector(`#id_subtotal`);
  let contact = document.querySelector(`#customer_box #id_contact`);
  
  subtotal.oninput = calculateTax;
  gw.oninput = calculateNetWeight;
  lw.oninput = calculateNetWeight;
  method.oninput = displayFields;
  contact.oninput = fetchCustomer;
  
  calulateTotals();
}


