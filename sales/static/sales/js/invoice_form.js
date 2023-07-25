function newRow(element, subform_name) {
  // let selected = document.querySelector(`#${subform_name}_table #selected`);

  // if (selected !== null) {
  //     selected.id = "";
  // }

  // let tbody = document.querySelector(`#${subform_name}_table tbody`);
  // let tr = document.querySelector(`#${subform_name}_table tbody tr:last-child`);
  // let clone = tr.cloneNode(true);

  // let changePrefixInputs = tr.querySelectorAll(`input[name^='${subform_name}-__prefix__']`);
  // changePrefixInputs.forEach( (input) => {
  //   let text = input.name;
  //   let result = text.replace("__prefix__", element.parentElement.rowIndex);
  //   input.setAttribute("name", result);
  // });
  // let total_forms = document.getElementById(`id_${subform_name}-TOTAL_FORMS`);
  // total_forms.value = parseInt(total_forms.value) + 1;

  // tbody.appendChild(clone);

  // tr.id = "selected";

  let form = document.getElementById(`${subform_name}_subform`);

  if (form.hidden) {
    form.hidden = false;
  }
  
  // tr.lastElementChild.children[0].style.display = "inline"; //Displaying cross button
}

function submitRow(element, subform_name) {

  if (subform_name == "products") {
    radioField = document.querySelector("#product_subform input[name='radio_type']:checked").value;
    subform_name = radioField == "tagged" ? "products" : "untagged";
  }

  let selected = document.querySelector(`#${subform_name}_table #selected`);

  if (selected !== null) {
    selected.id = "";
  }

  let tbody = document.querySelector(`#${subform_name}_table tbody`);
  let tr = document.querySelector(`#${subform_name}_table tbody tr:last-child`);
  let clone = tr.cloneNode(true);

  let changePrefixInputs = tr.querySelectorAll(`input[name^='${subform_name}-__prefix__']`);
  changePrefixInputs.forEach( (input) => {
    let text = input.name;
    let result = text.replace("__prefix__", element.parentElement.rowIndex);
    input.setAttribute("name", result);
  });
  let total_forms = document.getElementById(`id_${subform_name}-TOTAL_FORMS`);
  total_forms.value = parseInt(total_forms.value) + 1;

  tbody.appendChild(clone);
}

function updateValues(fromTable, subform_name, table_name) {
  let source = undefined;
  let dest = undefined;
  let split_character = undefined;
  if (fromTable) {
    source = document.querySelectorAll(`#${table_name}_table #selected input`);
    dest = document.querySelectorAll(`#${subform_name}_subform input, #${subform_name}_subform select`);
    source_split_func = (element) => element.name.split("-");
    dest_split_func = (element) => [element.name];
  }
  else {
    source = document.querySelectorAll(`#${subform_name}_subform input, #${subform_name}_subform select`);
    dest = document.querySelectorAll(`#${table_name}_table #selected input`);
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

function switchProductFields(element) {
  fields = ['metal', 'type', 'purity', 'category', 'pieces', 'gross_weight', 'less_weight', 'studs_weight', 'net_weight'];

  fieldHandler = (field, boolean) => {field.disabled = boolean; field.value = "";}

  if (element.value == "tagged") {
    fieldHandler(document.querySelector("#product_subform #id_id"), false);

    fields.forEach(field => fieldHandler(document.querySelector(`#product_subform #id_${field}`), true));
  }
  else {
    fieldHandler(document.querySelector("#product_subform #id_id"), true);

    fields.forEach(field => fieldHandler(document.querySelector(`#product_subform #id_${field}`), false));
  }
}
