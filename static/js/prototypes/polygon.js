function Polygon(map, editable, color){
    this.vertices = new google.maps.Polygon({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color===undefined ? '#FF0000':color,
        fillOpacity: 0.35,
        map: map
      })
    this.list_vertices = []
    this.active = true
    this.editable = editable===undefined ? true:editable;
    this.title = "poly"
}

Polygon.prototype.createVertices = function(position){
    if(this.editable){
        this.new_point = new Point_Marker(position, this.vertices.map)
        this.list_vertices.push(this.new_point)
        this.new_point.setTitle("Vertex "+this.TotalVertices())
        this.vertices.getPath().push(position)
    }
    else{
        this.vertices.getPath().push(position)
    }

}
Polygon.prototype.getListVertices= function(){
    return this.list_vertices
}
Polygon.prototype.TotalVertices = function(){
    return this.list_vertices.length
}
Polygon.prototype.findVertex = function(index){
    return this.list_vertices[index]
}
Polygon.prototype.getLastVertex = function(){
    return this.list_vertices[this.TotalVertices()-1]
}
Polygon.prototype.removeVertex = function(index){
    this.list_vertices[index].setMap(null)
    this.vertices.getPath().removeAt(index)
    this.list_vertices.splice(index,1);
    for(i in this.list_vertices){
        this.list_vertices[i].setTitle("Vertex "+(parseInt(i)+1))
    }
    
}
Polygon.prototype.getVertices = function(){
    return this.vertices.getPath()["i"]
}
Polygon.prototype.setVertexPosition = function(vert, position){
    this.vertices.getPath().setAt(vert, position);
}
Polygon.prototype.setActive = function(bool){
    this.active = bool
    var map = this.vertices.map
    this.vertices.setMap(null)
    var color = this.active===true? '#FF0000' : '#2F4F4F'
    this.vertices = new google.maps.Polygon({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        map: map
    })
    for (x=0;x<this.list_vertices.length;x++){
        this.vertices.getPath().push(this.list_vertices[x].getPosition())
        this.active===true? this.list_vertices[x].setMap(map) : this.list_vertices[x].setMap(null)
    }
    this.vertices.setMap(map)
}
Polygon.prototype.setPath = function(path){
    this.vertices.setPath(path)
}

Polygon.prototype.setTitle = function(title){
    this.title = title
}
Polygon.prototype.getTitle = function(){
    return this.title
}
Polygon.prototype.haveMarker = function(marker){
    have = google.maps.geometry.poly.containsLocation(marker, this.vertices)
    return have
}