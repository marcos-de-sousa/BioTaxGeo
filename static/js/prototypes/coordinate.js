function Coordinate(){
    this.degree = null;
    this.minute = null;
    this.second = null;
    this.decimal = null;
    this.hemisphere = null;
}

Coordinate.prototype.toDDMMSS = function(coordinate, type){
var value = coordinate.toString().split(".")
if(value[0].indexOf("-" > -1) && type=="lat"){
    value[0] = value[0]*-1
    this.hemisphere = "S"
}
else if(type == "lng"){
    value[0] = value[0]*-1
    this.hemisphere = "W"
}
else{
    this.hemisphere = type === "lat" ? "N" : "E"
}
this.degree = value[0]

if(this.degree.toString().length<2){ this.degree = "0"+this.degree.toString() }
value[1] = "0."+value[1]
this.minute = value[1]*60
var value2 = this.minute.toString().split(".")
this.minute = value2[0]
value2[1] = "0."+value2[1]
this.second = value2[1]*60
this.second = parseFloat(this.second.toFixed(2))

var coord = `${this.degree}° ${this.minute}' ${this.second}" ${this.hemisphere}`

return coord
}
Coordinate.prototype.toDDMM = function(coordinate, type){
    var value = coordinate.toString().split(".")
    if(value[0].indexOf("-" > -1) && type=="lat"){
        value[0] = value[0]*-1
        this.hemisphere = "S"
    }
    else if(type == "lng"){
        value[0] = value[0]*-1
        this.hemisphere = "W"
    }
    else{
        this.hemisphere = type === "lat" ? "N" : "E"
    }
    this.degree = value[0]
    if(this.degree.toString().length<2){ this.degree = "0"+this.degree.toString() }
    value[1] = "0."+value[1]
    this.minute = value[1]*60
    this.minute = parseFloat(this.minute.toFixed(3))
    
    var coord = `${this.degree}° ${this.minute}' ${this.hemisphere}`
    
    return coord
}