function addRow(element) {
    let selected = document.getElementById('selected');
    if (selected !== null) {
        selected.id = "";
    }
    if (element.id === "add") {
        let tbody = element.parentElement.parentElement;
        let clone = element.parentElement.cloneNode(true);
        let changePrefixInputs = element.parentElement.querySelectorAll("input[name^='partciulars-__prefix__']");
        changePrefixInputs.forEach( (input) => {
        let text = input.name;
        let result = text.replace("__prefix__", element.parentElement.rowIndex);
        input.setAttribute("name", result);
        });
        let total_forms = document.getElementById("id_particulars-TOTAL_FORMS");
        total_forms.value = parseInt(total_forms.value) + 1;
        tbody.appendChild(clone);
        element.id = "";
    }
    element.parentElement.id = "selected";
    element.innerHTML = element.parentElement.rowIndex;
    let form = document.getElementById('particular_subform');
    if (form.hidden) {
        form.hidden = false;
    }
    element.parentElement.lastElementChild.children[0].style.display = "inline"; //Displaying cross button
    updateValues(true);
}

function updateValues(fromTable) {
    let source = undefined;
    let dest = undefined;
    let split_character = undefined;
    if (fromTable) {
      source = document.querySelectorAll('#selected input');
      dest = document.querySelectorAll('#particular_subform input, #particular_subform select');
      source_split_func = (element) => element.name.split("-");
      dest_split_func = (element) => [element.name];
    }
    else {
      source = document.querySelectorAll('#particular_subform input, #particular_subform select');
      dest = document.querySelectorAll('#selected input');
      source_split_func = (element) => [element.name];
      dest_split_func = (element) => element.name.split("-");
    }

    for (let i = 0; i < source.length; i++) {
      let source_names = source_split_func(source[i]);
      let source_name = source_names[source_names.length - 1];
      for (let j = 0; j < dest.length; j++) {
        let dest_names = dest_split_func(dest[j]);
        let dest_name = dest_names[dest_names.length - 1];
        if (source_name == dest_name) {
          dest[j].value = source[i].value;
          if (source[i].tagName == "SELECT") {
            let input_of_select = dest[j].parentElement.querySelector('input');
            input_of_select.value = source[i].selectedOptions[0].text;
          }
          break;
        }
      }
    }
    calculateTotals();
}

function deleteRow(element) {
element.parentElement.parentElement.style.display = "none";
// TODO: Add logic to add Form-#-Delete to POST data
}

function calculateTotals() {
  let gross_weight = document.querySelector('#totals_box #id_gross_weight');
  console.log(gross_weight);
  let net_weight = document.querySelector('#totals_box #id_net_weight');
  let pure_weight = document.querySelector('#totals_box #id_pure_weight');
  let amount = document.querySelector('#totals_box #id_amount');
  let trs = document.querySelectorAll('#particular_form_table tbody tr');
  let gw = 0.0;
  let nw = 0.0;
  let pw = 0.0;
  let am = 0.0;
  for (let i = 0; i < trs.length; ++i) {
    gw += Number(trs[i].children[4].children[0].value);
    nw += Number(trs[i].children[5].children[0].value);
    pw += Number(trs[i].children[3].children[0].value) * Number(trs[i].children[5].children[0].value) / 100;
    am += Number(trs[i].children[9].children[0].value);
  }
  gross_weight.value = gw;
  net_weight.value = nw;
  pure_weight.value = pw;
  amount.value = am;
}

// TODO: Tax calculation function