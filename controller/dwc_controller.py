from flask import render_template, request, Blueprint, redirect, url_for, make_response
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet
import json
dwc_blueprint = Blueprint('dwc', __name__, template_folder='templates')
dwc_sheet = Sheet()

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
        list_scientificname = []
        keys = list(form.keys())
        for i in range(len(list_genus)):
            list_scientificname.append(list_genus[i]+" "+list_species[i])
        count = 0
        print(len(keys))
        print(list_scientificname)
        for i in range(len(dwc_titles)):
            if dwc_titles[i] == "scientificName":
                dwc_sheet.Change_Column(column=None, value=list_scientificname, index=i)
            elif dwc_titles[i] == "taxonRank":
                dwc_sheet.Change_Column(column=None, value=list_species, index=i)
            elif form[keys[count]] != "Select...":
                print(form[keys[count]])
                value = used_sheet.Value_in_Column(form[keys[count]])
                dwc_sheet.Change_Column(column=None, value=value, index=i)
                count += 1
            else:
                count += 1

        dwc_sheet.Save_Write_Spreadsheet(".xls", "DwC_Occurrence")
        return res