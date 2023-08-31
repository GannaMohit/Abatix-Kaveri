function newPaymentRow(element) {
  newRow(element, 'payments');
  displayFields();
}

function submitPaymentRow(element) {
  submitRow(element, 'payments', 'payments');
  calculateTotals();
}

function deletePaymentRow(element) {
  deleteRow(element);
  calculateTotals();
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

function calculateTotals() {
  let amount_inputs = document.querySelectorAll(`#payments_table #id_amount_table`);
  let delete_inputs = document.querySelectorAll(`#payments_table [name$='-DELETE']`);

  let amount = document.getElementById('id_amount_total');
  amount.innerText = `₹${Number(calulateTotal(amount_inputs, delete_inputs)).toFixed(2)}`;
}

window.onload = () => {
  disbaleEnter();
  let method = document.querySelector("#payment_subform #id_method");
  let contact = document.querySelector(`#customer_box #id_contact`);
  
  method.oninput = displayFields;
  contact.oninput = fetchCustomer;
}