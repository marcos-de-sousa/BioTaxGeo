function createPolygon() {

    var belem = {lat:-1.44502, lng: -48.4650};
    var map = new google.maps.Map(document.getElementById('first_map'), {zoom: 4, center: belem, gestureHandling: 'greedy'});
    var selected_polygon = new Polygon(map)

    var div_component = document.getElementById("insert_inputs")
    var btn_create_poly = document.getElementById("Btn_Create_Poly")
    var select_poly_component = document.getElementById("select_poly")
    var btn_create_vertex = document.getElementById("btn_create_vertex")
    var input_lat = document.getElementById("Latitude")
    var input_lng = document.getElementById("Longitude")
    var btn_save_coordinate = document.getElementById("btn_save_coord")
    var input_send_polygons = document.getElementById("send_polygons")

    var list_componentsHTML = []
    var list_polygons = []
    var polygon_components = {}
    var index_polygon = 0
    list_polygons.push(selected_polygon)

    function addVerticesPolygon(event){
        var new_components = new ComponentHTML()
        event.latLng===undefined ? vertex_lat = input_lat.value : vertex_lat = event.latLng.lat()
        event.latLng===undefined ? vertex_lng = input_lng.value : vertex_lng = event.latLng.lng()
        var coord =  new google.maps.LatLng(vertex_lat, vertex_lng)
        selected_polygon.createVertices(coord)
        var index = selected_polygon.TotalVertices()-1
        selected_polygon.getLastVertex().addListener('position_changed', MouseMovedVertex);
        selected_polygon.getLastVertex().setIndex(index)
        new_components.createInputGroup(vertex_lat, vertex_lng, index, div_component, InputMovedVertex, DeleteVertex)
        list_componentsHTML.push(new_components)
        polygon_components[`polygon${index_polygon}`] = {"polygon": selected_polygon, "components": list_componentsHTML}
    }
    function MouseMovedVertex(){
        var vertex = this
        var index_vertex = parseInt(vertex.getIndex())
        selected_polygon.setVertexPosition(index_vertex, vertex.getPosition())
        list_componentsHTML[index_vertex].setValueInputLat(vertex.getLatitude())
        list_componentsHTML[index_vertex].setValueInputLng(vertex.getLongitude())
    } 
    function InputMovedVertex(){
        var input = this
        var index = input.id.includes("Lat") ? input.id.replace("Lat", "") : input.id.replace("Lng", "")
        var vertex = selected_polygon.findVertex(index)
        selected_polygon.setVertexPosition(index, vertex.getPosition())
        if(input.id.includes("Lat")){
            vertex.setLatitude(parseFloat(input.value))
        }
        else{
            vertex.setLongitude(parseFloat(input.value))
        }
    }
    function DeleteVertex(){
        index = this.id.replace("Delete","")
        delete_input_group = list_componentsHTML[index].getSuperDiv()
        div_component.removeChild(delete_input_group)
        selected_polygon.removeVertex(index)
        RenameIDComponentsHTML(index)
        list_componentsHTML.splice(index,1)    
    }
    function CreatePolygon(){
        let create = true
        list_polygons.forEach(function(poly){ poly.TotalVertices() < 3 ? create = false:null  })
        if(create){
            var new_polygon = new Polygon(map)
            list_polygons.push(new_polygon)
            selected_polygon.setActive(false)
            selected_polygon = new_polygon
            index_polygon = list_polygons.length-1
            ClearDivComponent()
            list_componentsHTML = []
            polygon_components[`polygon${index_polygon}`] = {"polygon": selected_polygon, "components": list_componentsHTML}
            
            var new_components = new ComponentHTML()
            total_polygon = list_polygons.length
            new_components.createOption(index_polygon, "Polygon "+total_polygon, select_poly_component)
        }
        else{
            alert("To create a new polygon it is necessary that the current one has more than 2 vertices!")
        }

    }
    function SelectPolygon(){
        index_polygon = this.value
        if(index_polygon >=0){
            array_keys_polys = Object.keys(polygon_components)
            var picked_poly = array_keys_polys[index_polygon]
            selected_polygon.setActive(false);
            ClearDivComponent()
            list_componentsHTML = []
            selected_polygon = polygon_components[picked_poly]["polygon"];
            list_componentsHTML = polygon_components[picked_poly]["components"]
            for (x=0;x<list_componentsHTML.length;x++){
                div_component.appendChild(list_componentsHTML[x].getSuperDiv())
            }
            selected_polygon.setActive(true);
        }
    }
    function ClearDivComponent(){
        if(list_componentsHTML != []){
            for (x=0; x<list_componentsHTML.length; x++){
                child = list_componentsHTML[x].getSuperDiv()
                div_component.removeChild(child)
            }
        }
    }
    function RenameIDComponentsHTML(index){
        for (i=index;i<selected_polygon.TotalVertices();i++){
            ind = parseInt(i)
            list_componentsHTML[ind+1].setIDSuperDiv("input_vertex"+i)
            list_componentsHTML[ind+1].setIDInputLat("Lat"+i)
            list_componentsHTML[ind+1].setIDInputLng("Lng"+i)
            list_componentsHTML[ind+1].setIDButton("Delete"+i)
            list_componentsHTML[ind+1].setIDSpan("span"+i)
            list_componentsHTML[ind+1].setTextSpan((ind+1)+"ª. "+"Vertex")
            selected_polygon.getListVertices()[ind].setIndex(ind)
        }
    }
    function SavePolygonsVertices(){
        var send_polygons = {}
        for (polygon in polygon_components){
            send_polygons[polygon] = polygon_components[polygon]["polygon"].getVertices()
        }
        send_polygons = JSON.stringify(send_polygons)
        input_send_polygons.value = send_polygons
        alert("Coordinates Saved!")
    }

    map.addListener('click', addVerticesPolygon);
    btn_create_vertex.addEventListener('click', addVerticesPolygon);
    btn_create_poly.addEventListener('click', CreatePolygon);
    btn_save_coordinate.addEventListener('click', SavePolygonsVertices);
    select_poly_component.addEventListener('change', SelectPolygon);
}