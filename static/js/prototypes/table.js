function Table(){
    this.table;
    this.header = [[],[]];
    this.body = [[],[]];
    this.body_component;
}
Table.prototype.setTable = function (tableComponentHTML){
    this.table = tableComponentHTML;
}
Table.prototype.setHeader = function (trHead) {
    this.header[0].push(trHead);
}
Table.prototype.setBody = function (tBody) {
    this.body_component = tBody;
}
Table.prototype.getBody = function(){
    return this.body;
}
Table.prototype.createTitlesInHeader = function (arrThColumns, total_values) {
    for (value of arrThColumns){
        let th = document.createElement("th");

        th.setAttribute("scope","col");
        value += `: ${total_values}`
        th.innerHTML = value.charAt(0).toUpperCase()+value.slice(1); 
        this.header[1].push(th);
        this.header[0][0].appendChild(th);
    }
}
Table.prototype.createRowInBody = function (){
    let tr = document.createElement("tr");
    tr.setAttribute
    this.body[0].push(tr);
    this.body_component.appendChild(tr)
    this.body[1].push([])
}
Table.prototype.getAllRowBody = function () {
    return this.body[0]
}
Table.prototype.createColumnInBody = function (value) {
        let td = document.createElement("td");
        td.tagName = "cu"
        td.innerHTML = value
        last_row = this.body[0].length-1
        this.body[0][last_row].appendChild(td)
        this.body[1][last_row].push(td)
}
Table.prototype.setStyleTdBody = function (row, column, style){
    this.body[1][row][column].style = style;
}
Table.prototype.setAttributeTdBody = function (row, column, att, value){
     this.body[1][row][column].setAttribute(att, value);
}
Table.prototype.setEventTdBody = function (row, column, event_type, event){
     this.body[1][row][column].addEventListener(event_type, event);
}
Table.prototype.setClassNameTdBody = function (row, column, classs){
     this.body[1][row][column].className = classs;
}
Table.prototype.setIDTdBody = function (row, column, id){
     this.body[1][row][column].id = id; 
}
Table.prototype.setInnerHTMLTdBody = function (row, column, value){
     this.body[1][row][column].innerHTML = value;
}
Table.prototype.getInnerHTMLTdBody = function (row, column){
    return  this.body[1][row][column].innerHTML;
}
Table.prototype.findValueInRowBody = function (index_Row, value_to_find) {
    for (value of this.body[1][index_Row]){
        if (value.innerHTML == value_to_find){
            return value;
        }
    }
    return "not find";
}
Table.prototype.setClassNameRowBody = function (row, c){
    this.body[0][row].className = c;
}
