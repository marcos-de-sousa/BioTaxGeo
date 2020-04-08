var table = new Table();

Cancel_Buttom.addEventListener("click", InputsRemove)
Close_Buttom.addEventListener("click", InputsRemove)
table.setTable(table);
table.setHeader(thead);
table.setBody(tbody);
first_value = Object.keys(verified_hierarchy)[0]
Arr_Titles = Object.keys(verified_hierarchy[first_value])

table.createTitlesInHeader(Arr_Titles, TOTAL_ROWS);

for (key in verified_hierarchy){
  row = Object.keys(verified_hierarchy).indexOf(key)
  table.createRowInBody()
  table.setClassNameRowBody(row, "not_wrong")
  for (key2 in verified_hierarchy[key]){
    column = Object.keys(verified_hierarchy[key]).indexOf(key2)
    value = verified_hierarchy[key][key2]["type"]
    amount_value = verified_hierarchy[key][key2]["amount"]
    value += `: ${amount_value!=undefined?amount_value:0}`
    table.createColumnInBody(value)
    if(verified_hierarchy[key][key2]["correctness"] != "EXACT" && key2 != "scientific name"){
      table.setClassNameRowBody(row, "wrong")
      correctness = verified_hierarchy[key][key2]["correctness"]
      correctness == "FUZZY" ? table.setStyleTdBody(row, column, "color: orange;cursor: pointer;"):table.setStyleTdBody(row, column, "color: red;cursor: pointer;")
      table.setAttributeTdBody(row, column, "data-target","#exampleModal")
      table.setAttributeTdBody(row, column, "data-toggle","modal")
      table.setAttributeTdBody(row, column, "wrong","true")
      table.setEventTdBody(row, column, "click", ChangingDataLocalSheet)
      table.setClassNameTdBody(row, column, key2)
      table.setIDTdBody(row, column, key+key2)
    }
  }
}