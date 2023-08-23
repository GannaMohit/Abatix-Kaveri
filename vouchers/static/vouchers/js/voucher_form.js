function newParticularRow(element) {
  newRow(element, 'products');
}

function submitParticularRow(element) {
  radioField = document.querySelector("#product_subform input[name='radio_type']:checked").value;
  table_name = radioField == "tagged" ? "products" : "particular";
  subform_name = "products";

  submitRow(element, table_name, subform_name);
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

window.onload = () => {
  let type = document.querySelector("#voucher_box #id_type");
  type.oninput = changeVoucherNumber;
}

// TODO: Tax calculation function
// TODO: Total calculation function
// TODO: # calculation function