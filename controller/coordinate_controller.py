from flask import render_template, request, Blueprint, redirect, url_for, make_response
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet

coordinate_blueprint = Blueprint('coordinate', __name__, template_folder='templates')


@coordinate_blueprint.route("/coordinate_validation", methods=["GET", "POST"])
def coordinate_validation():
    if request.method == 'POST':
        form = request.form.to_dict()
        used_sheet.coordinate.set_Latitude_Column_values(form["latitude"])
        used_sheet.coordinate.set_Longitude_Column_values(form["longitude"])
        coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
        coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
        coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
        coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)
        if(form["coordinate_type"] == "Decimal"):
            used_sheet.Change_Column(form["latitude"], coord_lat, name="decimal_latitude")
            used_sheet.set_Columns_Total(used_sheet.get_Columns_Total() + 1)
            used_sheet.Change_Column(form["longitude"], coord_lng, name="decimal_longitude")
            used_sheet.Save_Formatted_Spreadsheet(form["type_file"])
            return redirect(url_for("home.home"))
        elif(form["coordinate_type"] == "MMDDSS"):
            lat_ddmmss = []
            lng_ddmmss = []
            for i in range(len(coord_lat)):
                lat_ddmmss.append(used_sheet.coordinate.toDDMMSS(coord_lat[i], "lat"))
                lng_ddmmss.append(used_sheet.coordinate.toDDMMSS(coord_lng[i], "lng"))
            used_sheet.Change_Column(form["latitude"], lat_ddmmss, name="DDMMSS_latitude")
            used_sheet.set_Columns_Total(used_sheet.get_Columns_Total()+1)
            used_sheet.Change_Column(form["longitude"], lng_ddmmss, name="DDMMSS_longitude")
            used_sheet.Save_Formatted_Spreadsheet(form["type_file"])
            return redirect(url_for("home.home"))
        elif(form["coordinate_type"] == "MMDD"):
            lat_ddmm = []
            lng_ddmm = []
            for i in range(len(coord_lat)):
                lat_ddmm.append(used_sheet.coordinate.toDDMM(coord_lat[i], "lat"))
                lng_ddmm.append(used_sheet.coordinate.toDDMM(coord_lng[i], "lng"))
            used_sheet.Change_Column(form["latitude"], lat_ddmm, name="DDMM_latitude")
            used_sheet.set_Columns_Total(used_sheet.get_Columns_Total() + 1)
            used_sheet.Change_Column(form["longitude"], lng_ddmm, name="DDMM_longitude")
            used_sheet.Save_Formatted_Spreadsheet(form["type_file"])
            return redirect(url_for("home.home"))
        return redirect(url_for("coordinate.coordinate_form"))