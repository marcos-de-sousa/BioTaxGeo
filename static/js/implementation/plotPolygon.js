function plotPolygon() {
    //var mapi = new google.maps.Map(document.getElementById("mapi"), {zoom: 4, center: belem});

    //__________________________________VARIÁVEIS GLOBAIS___________________________________________________________________
    var belem/*..............................*/= {lat:-1.44502, lng: -48.4650};
    var map/*................................*/= new google.maps.Map(document.getElementById('second_map'), {zoom: 4, center: belem, gestureHandling: 'greedy'});
    
    var CHECKBOX_ACTIVE_MARKERCLUSTER/*......*/= document.getElementById("checkbox");
        CHECKBOX_ACTIVE_MARKERCLUSTER.checked  = true;
    var Modal/*..............................*/= document.getElementById("modal_body");
    var BUTTOM_CANCEL/*......................*/= document.getElementById("Cancel_Buttom");
    var BUTTOM_CONFIRM/*.....................*/= document.getElementById("Confirm_Buttom");
    var BUTTOM_SAVE/*........................*/= document.getElementById("submit");
    var BUTTOM_CLOSE/*.......................*/= document.getElementById("close_x");
    var INPUT_DATA/*.........................*/= document.getElementById("data");
    var Geo/*................................*/= new google.maps.Geocoder;
    var COORDINATE_CONVERSOR/*...............*/= new Coordinate();
    var INPUT_RADIO/*........................*/= new ComponentHTML();
    var Send_Values_Server/*.................*/= {};
    var Values_To_Send/*.....................*/= {};
    var Column_Modify/*......................*/= "";
    var Column_Changed/*.....................*/= null;
    var Row_Modify/*.........................*/= null;
    var List_Poly/*.........................*/ = [];
    var List_Components_HTML/*..............*/ = [];
    var List_Marker/*.......................*/ = [];
    //_____________________________________________________________________________________________________________________
    
    
    //todos esses for são para verificar se há markers dentro de algum polígono
    for (poly in polygons){
        let selected_polygon = new Polygon(map)
        let header_table = new ComponentHTML()
        selected_polygon.setActive(false)
        selected_polygon.setPath(polygons[poly])
        List_Poly.push(selected_polygon)
        header_table.createHeaderTable("List of Markers within the Polygon "+List_Poly.length, List_Poly.length)
        header_table.createTitleTable()
        selected_polygon.setTitle("polygon"+List_Poly.length)
        List_Components_HTML.push(header_table)
    }
    for(i=0;i<latitudes.length;i++){
        if (latitudes[i]!=""){
            let coord = new google.maps.LatLng(latitudes[i], longitudes[i])
            let marker = new Point_Marker(coord, map, "../static/image/red_marker2.png" , false)
            List_Marker.push(marker)
        }
    }
    for(i=0;i<List_Marker.length;i++){
        for(p=0; p<List_Poly.length; p++){
            if(List_Poly[p].haveMarker(List_Marker[i].getPosition())){
                List_Marker[i].setIcon("../static/image/blue_marker2.png")
                List_Marker[i].setInsidePolygon(true)
                List_Marker[i].setTitle(`\tSpreadsheet info \nCountry: ${country[i]}\nState: ${state[i]}\nCounty: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                name = genus[i]+" "+specie[i]
                
                List_Components_HTML[p].createBodyTable(name, country[i], state[i], county[i], List_Marker[i].getLatitude(), List_Marker[i].getLongitude(), row_coord_lat[i], i, List_Poly[p].getTitle())


                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    List_Components_HTML[p].setIncorrectRow(List_Components_HTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    List_Components_HTML[p].setIncorrectRow(List_Components_HTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    List_Components_HTML[p].setWrongRow(List_Components_HTML[p].getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    List_Components_HTML[p].setIncorrectRow(List_Components_HTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
                
            }
        }
    }

    //Esse for específico é para verificar os que estão fora de qualquer
    MarkersOutPolygon = new ComponentHTML()
    MarkersOutPolygon.createHeaderTable("List of Markers outside Polygons", "Without", "red")
    MarkersOutPolygon.createTitleTable()
    for(i=0;i<List_Marker.length;i++){
            if(!List_Marker[i].isInsidePolygon()){
                name = genus[i]+" "+specie[i]
                List_Marker[i].setTitle(`\tSpreadsheet info \nCountry: ${country[i]}\nState: ${state[i]}\nCounty: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                MarkersOutPolygon.createBodyTable(name, country[i], state[i], county[i], List_Marker[i].getLatitude(), List_Marker[i].getLongitude(), row_coord_lat[i], i, "without")
                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  List_Marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), List_Marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
            }
    }
    var opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 60, maxZoom: 14, minimumClusterSize: 2}
    var markerCluster = new MarkerClusterer(map, List_Marker, opt_options);
    function ActiveMarkerCluster(){
        if(this.checked){
            opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 60, maxZoom: 14, minimumClusterSize: 2}
            markerCluster.setOptions(opt_options)
            markerCluster.repaint()
        }
        else{
            opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 1, maxZoom: 1, minimumClusterSize: 1}
            markerCluster.setOptions(opt_options)
            markerCluster.repaint()
        }
    }
    function ActiveModal(){
        let region = ["country", "state", "county"]
        let coordinates = ["latitude", "longitude"]
        let column = this.className
        let text = document.getElementById("modal_text")
        let index = this.id.replace(this.name, "")
        Row_Modify = row_coord_lat[index]
        Column_Changed = this.id
        Column_Modify = spreadsheet_titles[column]
        
        if(Send_Values_Server[Row_Modify] != undefined){
            Values_To_Send = Send_Values_Server[Row_Modify]
        }
        else{
            Values_To_Send = {}
        }
        if(region.indexOf(column) > -1){
            BUTTOM_CONFIRM.removeAttribute("disabled");
            if(column == "country"){
                text.innerHTML = `We have verified that your COUNTRY is incorrect.<br>We noticed that in your spreadsheet your column for the country contains the value: <b style='color: red;'>${country[index]}</b><br>While its coordinate represents the location: <b style='color: green;'>${list_region[index][column]}<b>`
                Values_To_Send[Column_Modify] = list_region[index][column]
            }
            else if(column == "state"){
                text.innerHTML = `We have verified that your STATE is incorrect.<br>We noticed that in your spreadsheet your column for the state contains the value: <b style='color: red;'>${state[index]}</b><br>While its coordinate represents the location: <b style='color: green;'>${list_region[index][column]}<b>`
                Values_To_Send[Column_Modify] = list_region[index][column]
            }
            else if(column == "county"){
                text.innerHTML = `We have verified that your COUNTY is incorrect.<br>We noticed that in your spreadsheet your column for the county contains the value: <b style='color: red;'>${county[index]}</b><br>While its coordinate represents the location: <b style='color: green;'>${list_region[index][column]}<b>`
                Values_To_Send[Column_Modify] = list_region[index][column]
            }

            div_aux = document.createElement("div")
            div_aux.style = "width: 465px; height: 200px;"
            div_aux.id = "Map_Aux"
            Modal.appendChild(div_aux)
            let mapStyle = [{
                'featureType': 'administrative',
                'elementType': 'geometry.stroke',
                'stylers': [{'color': '#FF0000'}]
              },{
                'featureType': 'landscape.natural',
                'elementType': 'geometry.stroke',
                'stylers': [{'color': '#FF0000'}]
              }];
      
            map_aux = new google.maps.Map(div_aux, {zoom: 12, center: List_Marker[index].getPosition(), styles: mapStyle,  gestureHandling: 'greedy'});
            marker = new Point_Marker(List_Marker[index].getPosition(), map_aux, "../static/image/green_marker.png" , false)
            marker.setTitle(`Coordinates\nLatitude: ${List_Marker[index].getLatitude()}\nLongitude: ${List_Marker[index].getLongitude()}`)
              
            let contentString = '<div id="content">'+'<p>Your coordinate points here</p>'+'</div>'
            let infowindow = new google.maps.InfoWindow({
                content: contentString
              });

            infowindow.open(map, marker);   
        }
        else if(coordinates.indexOf(column) > -1){
            BUTTOM_CONFIRM.setAttribute("disabled","");

            
            let CompRest = {
                   
                }
            let address = {"address": `${country[index]}, ${state[index]}, ${county[index]}`, "componentRestrictions": { 
                country: country[index],                                                
                administrativeArea: county[index],                                      
               }  } 
            Geo.geocode(address, function (a){
                coordinate = {"latitude": {"decimal": null, "MMDDSS": null, "MMDD": null}, "longitude":{"decimal": null, "MMDDSS": null, "MMDD": null}}               
                latitude = a[0]['geometry']['location']['lat']()
                longitude = a[0]['geometry']['location']['lng']()
                lat_lng = column == "latitude" ? "lat":"lng"
                coordinate[column]['decimal'] = lat_lng == "lat"? latitude:longitude
                coord_decimal = coordinate[column]['decimal']
                coordinate[column]['DDMMSS'] = COORDINATE_CONVERSOR.toDDMMSS(coord_decimal, lat_lng)
                coordinate[column]['DDMM'] = COORDINATE_CONVERSOR.toDDMM(coord_decimal, lat_lng)
                text.innerHTML = `We found that your coordinate might be incorrect.<br>The region reported in your spreadsheet is: ${country[index]}, ${state[index]}, ${county[index]}<br><br>While its coordinates point to: ${list_region[index]['country']}, ${list_region[index]['state']}, ${list_region[index]['county']}<br><br>The correct coordinates for this location are:<br><br>`
                
                decimal = coordinate[column]['decimal']
                DDMMSS = coordinate[column]['DDMMSS']
                DDMM = coordinate[column]['DDMM']
                INPUT_RADIO.createRadioInput(Modal, `Decimal ${column}: ${decimal}<br><br>`, decimal, SelectedRadio, column)
                INPUT_RADIO.createRadioInput(Modal, `MMDDSS ${column}: ${DDMMSS}<br><br>`, DDMMSS, SelectedRadio, column)
                INPUT_RADIO.createRadioInput(Modal, `MMDD ${column}: ${DDMM}<br><br>`, DDMM, SelectedRadio, column)
                div_aux = document.createElement("div")
                div_aux.style = "width: 465px; height: 200px;"
                div_aux.id = "Map_Aux"
                Modal.appendChild(div_aux)
                style = [{
                    "featureType": "administrative",
                    "elementType": "geometry.stroke",
                    "stylers": [
                      { "color": "#FF0000" }
                    ]
                  }]
                map_aux = new google.maps.Map(div_aux, {zoom: 12, center: a[0]['geometry']['location'],  gestureHandling: 'greedy', styles: style});
                marker = new Point_Marker(a[0]['geometry']['location'], map_aux, "../static/image/green_marker.png" , false)
                marker.setTitle(`Coordenadas\nLatitude: ${latitude}\nLongitude: ${longitude}`)
            
                let contentString = '<div id="content">'+'<p>The suggested coordinate points here</p>'+'</div>'
                let infowindow = new google.maps.InfoWindow({
                    content: contentString
                  });
    
                infowindow.open(map, marker);   
            
            })
        }
    }
    function RemoveRadioModal(){
        INPUT_RADIO.removeRadioInput(Modal)
        Modal.removeChild(document.getElementById("Map_Aux"))
    }
    function SelectedRadio(){
        BUTTOM_CONFIRM.removeAttribute("disabled");
        Column_Modify = spreadsheet_titles[this.id];
        Values_To_Send[Column_Modify] = this.value;
    }
    function SaveChange(){
        BUTTOM_SAVE.removeAttribute('disabled')
        var coord = ["latitude", "longitude"]
        var region = ["country", "state", "county"]
        var component = new ComponentHTML()
        var changed = document.getElementById(Column_Changed)
        component.removeStatusWrongRow(changed, Values_To_Send[Column_Modify], ActiveModal)
        Send_Values_Server[Row_Modify] = Values_To_Send
        INPUT_DATA.value = JSON.stringify(Send_Values_Server)

        if(region.indexOf(changed.className) > -1){
            var lat_id = changed.id.replace(changed.className, "latitude")
            var lng_id = changed.id.replace(changed.className, "longitude")
            var lat = document.getElementById(lat_id)
            var lng = document.getElementById(lng_id)
            component.removeStatusWrongRow(lat, lat.innerHTML, ActiveModal)
            component.removeStatusWrongRow(lng , lng.innerHTML, ActiveModal)
        }
        if(coord.indexOf(changed.className) > -1){
            var country_id = changed.id.replace(changed.className, "country")
            var state_id = changed.id.replace(changed.className, "state")
            var county_id = changed.id.replace(changed.className, "county")
            
            var country = document.getElementById(country_id)
            var state = document.getElementById(state_id)
            var county = document.getElementById(county_id)
            component.removeStatusWrongRow(country, country.innerHTML, ActiveModal)
            component.removeStatusWrongRow(state , state.innerHTML, ActiveModal)
            component.removeStatusWrongRow(county , county.innerHTML, ActiveModal)
        }
    }
    BUTTOM_CANCEL.addEventListener("click", RemoveRadioModal)
    BUTTOM_CONFIRM.addEventListener("click", RemoveRadioModal)
    BUTTOM_CLOSE.addEventListener("click", RemoveRadioModal)
    BUTTOM_CONFIRM.addEventListener("click", SaveChange)
    CHECKBOX_ACTIVE_MARKERCLUSTER.addEventListener('change', ActiveMarkerCluster)
}