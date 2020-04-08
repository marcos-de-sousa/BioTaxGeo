function ChangingDataLocalSheet(){
    // LOCAL VARIABLE
    let modal          = document.getElementById("modal_body")
    let text           = document.getElementById("modal_text")
    let text2          = document.createElement("label")
    let key1           = this.id.replace(this.className, "")
    let key2           = this.className
    let amount         = verified_hierarchy[key1][key2]["amount"]
    let keys           = Object.keys(verified_hierarchy[key1])
    let init           = keys.indexOf(key2)
    let correct_value  = verified_hierarchy[key1][key2]["suggestion"]
    let wrong_value    = this.innerHTML.replace(": "+amount, "");
    let isArray        = Array.isArray(correct_value)
    
    // GLOBAL VARIABLE =
    more_one           = true
    count              = 0
    count2             = 0
    wrong_cell         = this;
    super_row          = this.parentElement
    //____________________________________________
    if (correct_value.length > 0){
        text.innerHTML     = "We didn't find the "+wrong_value+" value in your reference spreadsheet, but we found similar values.<br>Do you want to change the value of <b><label style='color: orange;'>"+wrong_value+"</b> to:"
        text2.id           = "text_aux"
        text2.innerHTML    = "<br>Select the amount of values you want to change below: <br>"
        Confirm_Buttom.setAttribute("disabled", "")
          
        for (names of correct_value){
        let div = document.createElement("div")
        let input = document.createElement("input")
        let label = document.createElement("label")
        let number_id = count
    
        div.className = "form-check"
        div.id = "inputs"+number_id.toString()
        
        input.className = "form-check-input"
        input.type = "radio"
        input.name = "Radio"
        input.id = number_id
        input.value = "option"
        input.addEventListener("click", SelectedValue)
    
        label.className = "form-check-label"
        label.innerHTML = names
        label.style = "color: green;"
    
        div.appendChild(input)
        div.appendChild(label)
        modal.appendChild(div)
        count++
        }
        modal.appendChild(text2)
        for (key=init; key<keys.length-1; key++){
        let div = document.createElement("div")
        let input = document.createElement("input")
        let label = document.createElement("label")
    
        div.className = "form-check"
        div.id = "inputs_quant"+count2
        
        input.className = "form-check-input"
        input.type = "radio"
        input.name = "Radio2"
        input.id = keys[key]
        input.value = "option2"
        input.addEventListener("click", SelectedValueAmount)
        
        label.className = "form-check-label"
        label.for = count
        label.innerHTML = "Do you want to change <b>"+verified_hierarchy[key1][keys[key]]["amount"]+"</b> values in your spreadsheet at the level of "+keys[key]+"?"
        div.appendChild(input)
        div.appendChild(label)
        modal.appendChild(div)
        count2++
        }
    }
    else{
        Confirm_Buttom.setAttribute("disabled", "")
        text.innerHTML     = "We didn't find the "+wrong_value+" value in your reference spreadsheet."
    }


  }
function ChangingDataGBIF(){
    // LOCAL
    let level_editing = true;
    let modal         = document.getElementById("modal_body");
    let text          = document.getElementById("modal_text");
    let key1          = this.id.replace(this.className, "");
    let key2          = this.className;
    let amount        = verified_hierarchy[key1][key2]["amount"];
    let wrong_value   = this.innerHTML.replace(": "+amount, "");
    let correct_value = verified_hierarchy[key1][key2]["suggestion"];
    let keys          = Object.keys(verified_hierarchy[key1]);
    let init          = keys.indexOf(key2);
    let isArray       = Array.isArray(correct_value);
    //GLOBAL
    wrong_cell        = this;
    count             = 0;
    count2            = 0;
    super_row          = this.parentElement;
    //________________________________________________________________
    Confirm_Buttom.setAttribute("disabled", "");

    if(!(isArray)){
        more_one = false
        selected = 0
        if ( verified_hierarchy[key1]["scientific name"]["synonymous"] ) {
            let linkGbifSynom = "https://www.gbif.org/species/"+verified_hierarchy[key1]["scientific name"]["synonym"]
            let linkGbifAccept = "https://www.gbif.org/species/"+verified_hierarchy[key1]["scientific name"]["accept"]
            let CanonicalName = verified_hierarchy[key1]["scientific name"]["canonicalname"]
            let SpeciesName = verified_hierarchy[key1]["scientific name"]["speciesname"]
            text.innerHTML = `Source: ${verified_hierarchy[key1]['scientific name']['font']} <br>We verified that your species <a href=${linkGbifSynom} target="_blank">${CanonicalName}</a> is a <b>homotypical synonym</b> of <a href=${linkGbifAccept} target="_blank">${SpeciesName}</a>.<br>Do you want to change the value of <b><label style='color: #FFD700;'>${wrong_value}</label></b> to <b><label style='color: green;'>${correct_value}</label></b>?<br>Below is the amount of values you want to change: <br>`  
        } 
        else{
            let linkGbif = "https://www.gbif.org/species/"+verified_hierarchy[key1]["scientific name"]["accept"]
            fonte = verified_hierarchy[key1]["scientific name"]["font"] == "GBIF" ? `<a href=${linkGbif} target="_blank">GBIF</a>` : "Planilha"
            SpeciesName = verified_hierarchy[key1]["scientific name"]["speciesname"]
            text.innerHTML = "Source: "+fonte+"<br>The value "+wrong_value+" regarding your species "+SpeciesName+" might be <b>possibly wrong</b>.<br>Do you want to change the value of <b><label style='color: #f57600;'>"+wrong_value+"</label></b> to <b><label style='color: green;'>"+correct_value+"</label></b>?<br>Below is the amount of values you want to change: <br>" 
        }
    }
    else if (correct_value.length > 0){
        more_one = true
        if(verified_hierarchy[key1]["scientific name"]["synonymous"]){
            let CanonicalName = verified_hierarchy[key1]["scientific name"]["type"]
            text.innerHTML = "Source: "+verified_hierarchy[key1]["scientific name"]["font"]+"<br>We verified that your species "+CanonicalName+" is a <b>homotypical synonym</b>.<br>Do you want to change the value of <b><label style='color: #FFD700;'>"+wrong_value+"</b>, to:"
        }
        else{
            let CanonicalName = verified_hierarchy[key1]["scientific name"]["type"]
            text.innerHTML = "Source: "+verified_hierarchy[key1]["scientific name"]["font"]+"<br>We verified that your value "+wrong_value+" of your species "+CanonicalName+"  <b> might be wrong</b>.<br>Do you want to change the value of <b><label style='color: #f57600;'>"+wrong_value+"</b>, to: "
        }
        for (names of correct_value){
            div = document.createElement("div")
            div.className = "form-check"
            div.id = "inputs"+count
            input = document.createElement("input")
            input.className = "form-check-input"
            input.type = "radio"
            input.name = "Radio"
            input.id = count
            input.value = "option"
            input.addEventListener("click", SelectedValue)
            label = document.createElement("label")
            label.className = "form-check-label"
            label.for = count
            label.innerHTML = names
            label.style = "color: green;"
            div.appendChild(input)
            div.appendChild(label)
            modal.appendChild(div)
            count++
        }
        text2 = document.createElement("label")
        text2.id = "text_aux"
        text2.innerHTML += "<br>Select the amount of values you want to change below:<br>"
        modal.appendChild(text2)
    }
    else{
        level_editing = false
        more_one = false
        text.innerHTML = "It was not possible to find suggestions in the GBIF and your spreadsheet for corrections to the value of <b><label style='color: #ff0000;'>"+wrong_value+"</b>"
    }
    if(level_editing){
        for (key=init; key<keys.length-1; key++){
            div = document.createElement("div")
            div.className = "form-check"
            div.id = "inputs_quant"+count2
            input = document.createElement("input")
            input.className = "form-check-input"
            input.type = "radio"
            input.name = "Radio2"
            input.id = keys[key]
            input.value = "option2"
            input.addEventListener("click", SelectedValueAmount)
            label = document.createElement("label")
            label.className = "form-check-label"
            label.for = count
            label.innerHTML = "Do you want to change <b>"+verified_hierarchy[key1][keys[key]]["amount"]+"</b> values in your spreadsheet at the level of "+keys[key]+"?"
            div.appendChild(input)
            div.appendChild(label)
            modal.appendChild(div)
            count2++
        }
    }
}
function InputsRemove(){

    let modal = document.getElementById("modal_body")

    if(more_one && count>0){
        for(x=0; x<count; x++){
            var del = document.getElementById("inputs"+x)
            modal.removeChild(del)
        }
        for(x=0; x<count2; x++){
            var del2 = document.getElementById("inputs_quant"+x)
            modal.removeChild(del2)
        }
        modal.removeChild(document.getElementById("text_aux"))
    }
    else if (count2 > 0){
        for(x=0; x<count2; x++){
            var del2 = document.getElementById("inputs_quant"+x)
            modal.removeChild(del2)
        }
    }

    selected = -1
    selected_amount = -1
}
function SaveChange(){
    //LOCAL
    let submit_buttom = document.getElementById("submit")
    let key1 = wrong_cell.id.replace(wrong_cell.className, "")
    let key2 = wrong_cell.className
    let data = document.getElementById("data")
    //GLOBAL
    submit_buttom.removeAttribute("disabled")
    wrong_cell.setAttribute("data-toggle","");
    wrong_cell.setAttribute("data-target",""); 
    wrong_cell.setAttribute("wrong","false");
    wrong_cell.style = "color: black;"
    CheckValuesRow()
    if(changed_data[key1] == null){
        changed_data[key1] = {}
    }

    if(!more_one){
        if(changed_data[key1][key2] == null){
            changed_data[key1][key2] = {}
        }
        changed_data[key1][key2] =  {"suggestion":verified_hierarchy[key1][key2]["suggestion"], "level": [selected_amount, verified_hierarchy[key1][selected_amount]["type"]]}
        wrong_cell.innerHTML = verified_hierarchy[key1][key2]["suggestion"]+": "+verified_hierarchy[key1][key2]["amount"];
        verified_hierarchy[key1][key2]["type"] = verified_hierarchy[key1][key2]["suggestion"]
    }
    else{
        if(changed_data[key1][key2] == null){
            changed_data[key1][key2] = {}
        }
        changed_data[key1][key2] =  {"suggestion": verified_hierarchy[key1][key2]["suggestion"][selected], "level": [selected_amount, verified_hierarchy[key1][selected_amount]["type"]]}
        wrong_cell.innerHTML = verified_hierarchy[key1][key2]["suggestion"][selected]+": "+verified_hierarchy[key1][key2]["amount"];
        verified_hierarchy[key1][key2]["type"] = verified_hierarchy[key1][key2]["suggestion"][selected]
    }
    verified_hierarchy[key1][key2]["correctness"] = "EXACT"
    verified_hierarchy[key1]["scientific name"]["correctness"] = "EXACT"
    InputsRemove()
    send_values = JSON.stringify(changed_data)
    data.value =  send_values
    if(only_wrong){
        ShowOnlyWrong()
    }
}
function SelectedValue(){
    selected = this.id;
    BothSelected()
}
function SelectedValueAmount(){
    selected_amount = this.id;
    BothSelected()
}
function BothSelected(){
    if (selected != -1 && selected_amount!= -1){
        Confirm_Buttom.removeAttribute("disabled")
    }
}
function ShowOnlyWrong(){
    for (element of document.getElementsByClassName("not_wrong")){
        element.setAttribute("hidden", "hidden")
    }
    only_wrong = true
}
function ShowAllValues(){
    for (element of document.getElementsByClassName("not_wrong")){
        element.removeAttribute("hidden")
    }
    only_wrong = false
}
function CheckValuesRow(){
    super_row.className = "not_wrong"
    for(element of super_row.childNodes){
        isWrong = JSON.parse(element.getAttribute("wrong"))
        if(isWrong){
            super_row.className = "wrong"
        }
    }
}