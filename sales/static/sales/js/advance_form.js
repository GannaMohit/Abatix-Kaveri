function addRow(element) {
  let selected = document.getElementById('selected');
  if (selected !== null) {
    selected.id = "";
  }
  if (element.id === "add") {
    let tbody = element.parentElement.parentElement;
    let clone = element.parentElement.cloneNode(true);
    let changePrefixInputs = element.parentElement.querySelectorAll("input[name^='payments-__prefix__']");
    changePrefixInputs.forEach( (input) => {
      let text = input.name;
      let result = text.replace("__prefix__", element.parentElement.rowIndex);
      input.setAttribute("name", result);
    });
    let total_forms = document.getElementById("id_payments-TOTAL_FORMS");
    total_forms.value = parseInt(total_forms.value) + 1;
    tbody.appendChild(clone);
    element.id = "";
  }
  element.parentElement.id = "selected";
  element.innerHTML = element.parentElement.rowIndex + 1;
  let form = document.getElementById('form-hidden');
  if (form.hidden) {
    form.hidden = false;
  }
  element.parentElement.lastElementChild.children[0].style.display = "inline"; //Displaying cross button
  displayFields(element.parentElement.children[1].children[0].value); //Passing method value
  updateValues(true);
}

function changeFields(element) {
  document.querySelector('#selected input[id$=method]').value = element.value;
  displayFields(element.value);
  updateValues(false);
}

function updateValues(fromTable) {
  let source = undefined;
  let dest = undefined;
  let split_character = undefined;
  if (fromTable) {
    source = document.querySelectorAll('#selected input');
    dest = document.getElementsByClassName('box_1_inputs');
    split_character = "-";
  }
  else {
    source = document.getElementsByClassName('box_1_inputs');
    dest = document.querySelectorAll('#selected input');
    split_character = "_";
  }
  for (let i = 0; i < source.length; i++) {
    let names = source[i].id.split(split_character);
    let name = names[names.length - 1];
    for (let j = 0; j < dest.length; j++) {
      if (dest[j].id.endsWith(name)) {
        dest[j].value = source[i].value;
        break;
      }
    }
  }
  //calculateTotals();
}

function deleteRow(element) {
  element.parentElement.parentElement.style.display = "none";
  // TODO: Add logic to add Form-#-Delete to POST data
}

function calculateTotals() {
  let total = document.getElementById('total');
  let trs = document.getElementById('table').children[0].children;
  let temp = 0.0;
  for (let i = 0; i < trs.length; ++i) {
    temp += Number(trs[i].children[4].children[0].value);
  }
  total.value = temp;
}

function displayFields(method) {
  let box_1_labels = document.getElementsByClassName('box_1_labels');
  let box_1_inputs = document.getElementsByClassName('box_1_inputs');
  for (let i = 0; i < box_1_inputs.length; ++i) {
    box_1_inputs[i].value = "";
    box_1_inputs[i].style.display = "none";
    box_1_labels[i].style.display = "none";
  }

  let input_date = document.querySelector("#id_payment_date");
  let label_input_date = document.querySelector("label[for='id_date']");

  let input_name = document.querySelector("#id_name");
  let label_input_name = document.querySelector("label[for='id_name']");

  let input_amount = document.querySelector("#id_payment_amount");
  let label_input_amount = document.querySelector("label[for='id_amount']");

  input_date.style.display = "inline-flex";
  label_input_date.style.display = "inline-flex";
  input_name.style.display = "inline-flex";
  label_input_name.style.display = "inline-flex";
  input_amount.style.display = "inline-flex";
  label_input_amount.style.display = "inline-flex";

  switch(method) {
    case "Cash": {
      break;
    }
    case "Credit Card":
    case "Debit Card": {
      let card_inputs = document.querySelectorAll("input[id^='id_card_']");
      let card_labels = document.querySelectorAll("label[for^='id_card_']");
      for (let i = 0; i < card_inputs.length; i++) {
        card_inputs[i].style.display = "inline-flex";
        card_labels[i].style.display = "inline-flex";
      }
      break;
    }
    case "Cheque": {
      let cheque_inputs = document.querySelectorAll("input[id^='id_cheque_']");
      let cheque_labels = document.querySelectorAll("label[for^='id_cheque_']");
      for (let i = 0; i < cheque_inputs.length; i++) {
        cheque_inputs[i].style.display = "inline-flex";
        cheque_labels[i].style.display = "inline-flex";
      }
      break;
    }
    case "IMPS":
    case "NEFT":
    case "RTGS": {
      let wire_inputs = document.querySelectorAll("input[id^='id_wire_']");
      let wire_labels = document.querySelectorAll("label[for^='id_wire_']");
      for (let i = 0; i < wire_inputs.length; i++) {
        wire_inputs[i].style.display = "inline-flex";
        wire_labels[i].style.display = "inline-flex";
      }
      break;
    }
    case "UPI": {
      let upi_inputs = document.querySelectorAll("input[id^='id_upi_']");
      let upi_labels = document.querySelectorAll("label[for^='id_upi_']");
      for (let i = 0; i < upi_inputs.length; i++) {
        upi_inputs[i].style.display = "inline-flex";
        upi_labels[i].style.display = "inline-flex";
      }
      break;
    }
    default: {}
  }
}

//window.addEventListener("pageshow", calculateTotals);
