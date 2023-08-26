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
    let result = text.replace("__prefix__", tr.rowIndex);
    input.setAttribute("name", result);
  });
  let total_forms = document.getElementById(`id_${table_name}-TOTAL_FORMS`);
  total_forms.value = parseInt(total_forms.value) + 1;

  tbody.appendChild(clone);
  tr.id = "selected";
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
    // TODO: Add logic to add Form-#-Delete to POST data
    let delete_field = tr.querySelector("input[name$='-DELETE']");
    delete_field.checked = true;
    tr.style.display = "none";
}

function validateFunction(element, url, string, field) {
    let subform_name = `${string}s`;
    element.setCustomValidity("");
    element.reportValidity();
    let inputs = document.querySelectorAll(`#${subform_name}_table [name$='-product']`);
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
        element.setCustomValidity(`The ${string} is already used.`)
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
    if (inputs[i].value != '') {
      if (Boolean(deletes[i].checked) == false) {
        val += inputs[i].value;
      }
    }
  }
  return val;
}

// document.addEventListener("keydown", function(event) {
//   if (event.key === "Enter") {
//     event.preventDefault();
//     document.dispatchEvent( new KeyboardEvent( 'keydown', { 'key': "Tab" } ) );
//   }
// });