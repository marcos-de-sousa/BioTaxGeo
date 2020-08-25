from flask import render_template, request, Blueprint, redirect, url_for, make_response
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet
from model.date import Date
from model.coordinate import Coordinate
import json

dwc_blueprint = Blueprint('dwc', __name__, template_folder='templates')
dwc_sheet = Sheet()
date = Date()
coordinate = Coordinate(used_sheet)

@dwc_blueprint.route("/dwc_validation", methods=["GET", "POST"])
def dwc_validation():
    if request.method == 'POST':
        form = request.form.to_dict()
        titles = json.dumps(form)
        res = make_response(redirect(url_for("home.home")))
        res.set_cookie("titles_dwc", titles)
        dwc_titles = ["OccurrenceID", "basisOfRecord", "eventDate", "scientificName", "kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "taxonRank", "decimalLatitude", "decimalLongitude", "geodeticDatum", "countryCode"]
        dwc_sheet.create_WriteFile()
        dwc_sheet.create_SheetWriteFile("Occurrence")
        dwc_sheet.set_HeaderWriteFile(dwc_titles)
        list_genus = used_sheet.Value_in_Column(form["genus"])
        list_species = used_sheet.Value_in_Column(form["species"])
        list_latitude = used_sheet.Value_in_Column(form["latitude"])
        list_longitude = used_sheet.Value_in_Column(form["longitude"])
        list_date = used_sheet.Value_in_Column(form["eventdate"])
        list_decimal_latitude = []
        list_decimal_longitude = []
        list_scientificname = []
        list_new_date = []
        list_geodeticdatum = ["WGS84"]*len(list_longitude)

        for i in range(len(list_latitude)):
            list_decimal_latitude.append(coordinate.Convert_Lat_Decimal(list_latitude[i]))
            list_decimal_longitude.append(coordinate.Convert_Lng_Decimal(list_longitude[i]))
            if list_longitude[i] == "":
                list_geodeticdatum[i] = ""
        for d in list_date:
            new_date = date.toAAAAMMDD(d, "-", "DDMMAAAA")
            list_new_date.append(new_date["date"])
        keys = list(form.keys())
        for i in range(len(list_genus)):
            list_scientificname.append(list_genus[i]+" "+list_species[i])
        count = 0
        for i in range(len(dwc_titles)):
            if dwc_titles[i] == "scientificName":
                dwc_sheet.Change_Column(column=None, value=list_scientificname, index=i)
            elif dwc_titles[i] == "taxonRank":
                dwc_sheet.Change_Column(column=None, value=list_species, index=i)
            elif dwc_titles[i] == "geodeticDatum":
                dwc_sheet.Change_Column(column=None, value=list_geodeticdatum, index=i)
            elif form[keys[count]] != "Select...":
                if keys[count] == "latitude":
                    dwc_sheet.Change_Column(column=None, value=list_decimal_latitude, index=i)
                elif keys[count] == "longitude":
                    dwc_sheet.Change_Column(column=None, value=list_decimal_longitude, index=i)
                elif keys[count] == "eventdate":
                    dwc_sheet.Change_Column(column=None, value=list_new_date, index=i)
                else:
                    value = used_sheet.Value_in_Column(form[keys[count]])
                    if value != "Not found.":
                        dwc_sheet.Change_Column(column=None, value=value, index=i)
                count += 1
            else:
                count += 1

        dwc_sheet.Save_Write_Spreadsheet(".xls", "DwC_Occurrence")
        return res