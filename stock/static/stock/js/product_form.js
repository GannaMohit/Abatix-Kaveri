function changeValues(element) {
  let selected = document.getElementById('selected');
  if (selected !== null) {
    selected.id = "";
  }
  if (element.innerHTML === "Add") {
    let tbody = element.parentElement.parentElement;
    let clone = element.parentElement.cloneNode(true);
    tbody.appendChild(clone);
    let changePrefixInputs = element.parentElement.querySelectorAll("input[name^='studs-__prefix__']");
    changePrefixInputs.forEach( (input) => {
      let text = input.name;
      let result = text.replace("__prefix__", element.parentElement.rowIndex);
      input.setAttribute("name", result);
    });
    let total_forms = document.getElementById("id_studs-TOTAL_FORMS");
    total_forms.value = parseInt(total_forms.value) + 1;

  }
  element.parentElement.id = "selected";
  let form = document.getElementById('form-hidden');
  if (form.hidden) {
    form.hidden = false;
  }
  let tds = element.parentElement.children;
  tds[0].innerHTML = element.parentElement.rowIndex + 1;
  let inputs = document.getElementsByClassName('last-box-inputs');

  inputs[0].value = tds[1].children[1].value;
  inputs[1].checked = tds[2].children[0].value === "True" ? true: false;
  inputs[2].value = tds[3].children[0].value;
  inputs[3].value = tds[4].children[0].value;
  inputs[4].value = tds[5].children[0].value;
  inputs[5].value = tds[6].children[0].value;
  inputs[6].value = tds[6].children[2].value;
  inputs[7].value = tds[7].children[0].value;
  inputs[8].value = tds[8].children[0].value;
}

function updateTable(element) {
  let selected = document.getElementById('selected');
  let tds = selected.children;
  let inputs = document.getElementsByClassName('last-box-inputs');
  tds[1].children[0].value = inputs[0].options.selectedIndex === -1 ? "": inputs[0].selectedOptions[0].text;
  tds[1].children[1].value = inputs[0].value;
  tds[2].children[0].value = inputs[1].checked ? "True": "False";
  tds[3].children[0].value = inputs[2].value;
  tds[4].children[0].value = inputs[3].value;
  tds[5].children[0].value = inputs[4].value;
  tds[6].children[0].value = inputs[5].value;
  tds[6].children[1].value = inputs[6].options.selectedIndex === -1 ? "": inputs[6].selectedOptions[0].text;
  tds[6].children[2].value = inputs[6].value;
  tds[7].children[0].value = inputs[7].value;
  tds[8].children[0].value = inputs[8].value;
}

function calculateLessWeight(units) {
  let trs = document.getElementsByClassName('second-row-tables')[0].children[0].children;
  let less = 0;
  let studding = 0;
  let value = 0;
  for (let i = 0; i < trs.length; ++i) {
    let tds = trs[i].children;
    if (tds !== undefined) {
      if (tds[6].children[1].value !== "") {
        value = units.find(unit => unit["fields"]["symbol"] === tds[6].children[1].value)["fields"]["value_gram"] * tds[6].children[0].value;
        if (tds[2].children[0].value === "True") {
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
  //gw.value = Number(gw.value).toFixed(2);
  s.value = studding.toFixed(2);
  lw.value = less.toFixed(2);
  nw.value = (gw.value - less).toFixed(2);
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

document.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.dispatchEvent( new KeyboardEvent( 'keydown', { 'key': "Tab" } ) );
  }
});
