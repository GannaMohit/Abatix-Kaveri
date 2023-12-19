function newStudRow(element) {
  let subform_name = 'studs';
  newRow(element, subform_name);
}

function submitStudRow(element) {
  submitRow(element, "studs", "studs");
  calculateLessWeight();
  setSerialNumber('studs');
}

function deleteStudRow(element) {
  deleteRow(element);
  calculateLessWeight();
}

function calculateLessWeight() {
  let url = '/masters/_fetch_units'
  let csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
  let headers = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    }
  }
  let units = null;

  fetch(url, headers)
  .then(response => response.json())
  .then(function(units_ajax) {
    units = units_ajax.units;
    let weight_inputs = document.querySelectorAll(`#studs_table [name$='-weight']`);
    let unit_inputs = document.querySelectorAll(`#studs_table [name$='-unit']`);
    let less_inputs = document.querySelectorAll(`#studs_table [name$='-less']`);
    let delete_inputs = document.querySelectorAll(`#studs_table [name$='-DELETE']`);

    let less = 0;
    let studding = 0;
    let value = 0;
    for (let i = 0; i < weight_inputs.length; ++i) {
      if (weight_inputs[i].value != '') {
        if (Boolean(delete_inputs[i].checked) == false) {
          value = units.find(unit => unit["pk"] == unit_inputs[i].value)["fields"]["value_gram"] * weight_inputs[i].value;
          if (Boolean(less_inputs[i].checked) == true) {
            less += value;
          }
          studding += value;
        }
      }
    }

    let gw = document.getElementById('id_gross_weight');
    let s = document.getElementById('id_studs_weight');
    let lw = document.getElementById('id_less_weight');
    let nw = document.getElementById('id_net_weight');
    s.value = studding.toFixed(2);
    lw.value = less.toFixed(2);
    nw.value = (gw.value - less).toFixed(2);
  });
}

function makeRequired(element) {
  let making_charges = document.getElementById('id_making_charges');
  let wastage = document.getElementById('id_wastage');
  let mrp = document.getElementById('id_mrp');
  making_charges.required = false;
  wastage.required = false;
  mrp.required = false;
  if (element.value === "Making Charges") {
    making_charges.required = true;
  }
  else if (element.value === "Wastage") {
    wastage.required = true;
  }
  else if (element.value === "MRP") {
    mrp.required = true;
  }
}

window.onload = () => {
  disbaleEnter();
  makeRequired(document.querySelector("input[name='calculation']"));
  let gross_weight = document.querySelector("#id_gross_weight");
  gross_weight.oninput = calculateLessWeight;
}
