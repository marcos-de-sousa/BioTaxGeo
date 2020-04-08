function Localitys(country, state, county, locality){
    this.country = country || null
    this.state = state || null
    this.county = county || null
    this.locality_name = locality || null
}
Localitys.prototype.getCountry = function(){
    return this.country
}
Localitys.prototype.getState = function(){
    return this.state
}
Localitys.prototype.getCounty = function(){
    return this.county
}
Localitys.prototype.getLocalityName = function(){
    return this.locality_name
}
Localitys.prototype.getCompleteLocality = function(){
    complete_local = {
        "country": this.country,
        "state": this.state,
        "county": this.county,
        "Locality": this.locality_name
    }
    return complete_local
}