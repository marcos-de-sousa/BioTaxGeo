var table = new Table();

Cancel_Buttom.addEventListener("click", InputsRemove)
Close_Buttom.addEventListener("click", InputsRemove)
table.setTable(table);
table.setHeader(thead);
table.setBody(tbody);
first_value = Object.keys(verified_hierarchy)[0]
Arr_Titles = Object.keys(verified_hierarchy[first_value])

table.createTitlesInHeader(Arr_Titles, TOTAL_ROWS);
document.createElement("td").removeAttribute
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
    if(verified_hierarchy[key][key2]["correctness"] != "EXACT" && verified_hierarchy[key][key2]["correctness"] != "100%" && key2 != "scientific name"){
      is_array = Array.isArray(verified_hierarchy[key][key2]["suggestion"])
      array_count = is_array ? verified_hierarchy[key][key2]["suggestion"].length:null
      table.setClassNameRowBody(row, "wrong")
      if (verified_hierarchy[key]["scientific name"]["synonymous"]){
        table.setStyleTdBody(row, column, "color: #FFD700;cursor: pointer;")
      } else if ( !is_array ) {
        table.setStyleTdBody(row, column, "color: #f57600;cursor: pointer;")
      } else if ( array_count > 0 ) {
        table.setStyleTdBody(row, column, "color: #f57600;cursor: pointer;")
      } else {
        table.setStyleTdBody(row, column, "color: #ff0000;cursor: pointer;")   
      } 
      table.setAttributeTdBody(row, column, "data-target","#exampleModal")
      table.setAttributeTdBody(row, column, "data-toggle","modal")
      table.setAttributeTdBody(row, column, "wrong","true")
      table.setEventTdBody(row, column, "click", ChangingDataGBIF)
      table.setClassNameTdBody(row, column, key2)
      table.setIDTdBody(row, column, key+key2)
    }
  }
}