function newParticularRow(element) {
  newRow(element, 'products');
}

function submitParticularRow(element) {
  radioField = document.querySelector("#product_subform input[name='radio_type']:checked").value;
  table_name = radioField == "tagged" ? "products" : "particulars";
  subform_name = "products";

  submitRow(element, table_name, subform_name);
  setSerialNumber(table_name);
  calculateTaxTable();
  calulateTotals();
}

function deleteParticularRow(element) {
  deleteRow(element);
  calulateTotals();
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

function validateProductID(element) {
  validateFunction(element, '/stock/_fetch_product', "product", 'sold');
}

function changeVoucherNumber() {
  let type = document.querySelector("#voucher_box #id_type");
  let voucher_number = document.querySelector("#voucher_box #id_voucher_number");

  let issue = document.querySelector("#id_voucher_number_issue");
  let receive = document.querySelector("#id_voucher_number_receive");
  let urd = document.querySelector("#id_voucher_number_urd");

  switch (type.value) {
    case "Issue": 
      voucher_number.value = issue.value;
      break;
    case "Receive": 
      voucher_number.value = receive.value;
      break;
    case "URD":
      voucher_number.value = urd.value;
      break;
    default:
      break;
  }
}

function calculateTaxTable() {
  let tax_tables = document.querySelectorAll('.products_table #id_tax_table');
  let sgst_inputs = document.querySelectorAll(`.products_table [name$='-sgst']`);
  let cgst_inputs = document.querySelectorAll(`.products_table [name$='-cgst']`);
  let igst_inputs = document.querySelectorAll(`.products_table [name$='-igst']`);

  for (let i = 0; i < tax_tables.length - 1; i++) {
    if (sgst_inputs[i].value != '') {
      tax_tables[i].innerText = Number(Number(sgst_inputs[i].value)+Number(cgst_inputs[i].value)+Number(igst_inputs[i].value)).toFixed(0);
    }
  }
}

function calulateTotals() {
  let gross_weight_inputs = document.querySelectorAll(`.products_table #id_gross_weight_table`);
  let net_weight_inputs = document.querySelectorAll(`.products_table #id_net_weight_table`);
  let purity_inputs = document.querySelectorAll(`.products_table #id_purity_table`);
  let total_inputs = document.querySelectorAll(`.products_table #id_total_table`);
  let delete_inputs = document.querySelectorAll(`.products_table [name$='-DELETE']`);

  let pure_weight_inputs = [];
  for (let i = 0; i < purity_inputs.length; i++) {
    pure_weight_inputs.push({'innerText': Number(net_weight_inputs[i].innerText) * Number(purity_inputs[i].innerText) / 100});
  }

  let gw = document.getElementById('id_gross_weight_total');
  let nw = document.getElementById('id_net_weight_total');
  let pw = document.getElementById('id_pure_weight_total');
  let tot = document.getElementById('id_total_total');
  gw.innerText = `${Number(calulateTotal(gross_weight_inputs, delete_inputs)).toFixed(3)} g`;
  nw.innerText = `${Number(calulateTotal(net_weight_inputs, delete_inputs)).toFixed(3)} g`;
  pw.innerText = `${Number(calulateTotal(pure_weight_inputs, delete_inputs)).toFixed(3)} g`;
  tot.innerText = `₹${Number(calulateTotal(total_inputs, delete_inputs)).toFixed(2)}`;
}

window.onload = () => {
  let type = document.querySelector("#voucher_box #id_type");
  let gw = document.getElementById('id_gross_weight');
  let lw = document.getElementById('id_less_weight');
  let subtotal = document.querySelector(`#id_subtotal`);

  subtotal.oninput = calculateTax;
  gw.oninput = calculateNetWeight;
  lw.oninput = calculateNetWeight;
  type.oninput = changeVoucherNumber;
}