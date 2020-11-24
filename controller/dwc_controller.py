from flask import request, Blueprint, redirect, url_for, make_response
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet
from model.date import Date
from model.coordinate import Coordinate
import json, csv
import pandas as pd
import pycountry
from zipfile import ZipFile

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
        dwc_titles = ["occurrenceID", "basisOfRecord", "eventDate", "scientificName", "kingdom", "phylum", "class",
                      "order", "family", "genus", "specificEpithet", "taxonRank", "decimalLatitude", "decimalLongitude",
                      "geodeticDatum", "countryCode"]
        dwc_sheet.create_WriteFile()
        dwc_sheet.create_SheetWriteFile("Occurrence")
        dwc_sheet.set_HeaderWriteFile(dwc_titles)
        list_genus = used_sheet.Value_in_Column(form["genus"])
        list_species = used_sheet.Value_in_Column(form["species"])
        list_latitude = used_sheet.Value_in_Column(form["latitude"])
        list_longitude = used_sheet.Value_in_Column(form["longitude"])
        list_date = used_sheet.Value_in_Column(form["eventdate"])
        list_country = used_sheet.Value_in_Column(form["countrycode"])
        list_decimal_latitude = []
        list_decimal_longitude = []
        list_scientificname = []
        list_new_date = []
        list_formated_country = []
        list_geodeticdatum = ["WGS84"] * len(list_longitude)

        #  CREATE CSV DWC FILE
        for country in list_country:
            if str(country).lower() != "brasil":
                formated_country = pycountry.countries.get(name=country).alpha_2
                list_formated_country.append(formated_country)
            else:
                formated_country = "BR"
                list_formated_country.append(formated_country)

        for i in range(len(list_latitude)):
            list_decimal_latitude.append(coordinate.Convert_Lat_Decimal(list_latitude[i]))
            list_decimal_longitude.append(coordinate.Convert_Lng_Decimal(list_longitude[i]))
            if list_longitude[i] == "":
                list_geodeticdatum[i] = ""
        for d in list_date:
            new_date = date.toAAAAMMDD(d, ".", "DDMMAAAA")
            if "date" in new_date:
                list_new_date.append(new_date["date"])
            else:
                list_new_date.append(new_date)
        keys = list(form.keys())
        for i in range(len(list_genus)):
            list_scientificname.append(list_genus[i] + " " + list_species[i])
        count = 0
        for i in range(len(dwc_titles)):
            if dwc_titles[i] == "scientificName":
                dwc_sheet.Change_Column(column=None, value=list_scientificname, index=i)
            elif dwc_titles[i] == "taxonRank":
                dwc_sheet.Change_Column(column=None, value=list_species, index=i)
            elif dwc_titles[i] == "countryCode":
                dwc_sheet.Change_Column(column=None, value=list_formated_country, index=i)
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
        dwc_sheet.Save_Write_Spreadsheet(".csv", "DwC_Occurrence")

        # CREATE TXT FILE
        dwc_sheet_saved = "files/DwC_Occurrence.csv"
        txt_file = "DwC_Occurrence.txt"
        with open(txt_file, "w") as my_output_file:
            with open(dwc_sheet_saved) as my_input_file:
                [my_output_file.write(" ".join(row) + '\n') for row in csv.reader(my_input_file)]
            my_output_file.close()

        # CREATE XML DWC FILE
        df = pd.read_csv(dwc_sheet_saved, sep='|')
        index = 1
        data = []
        for row in df:
            data.append(row)
        data = data[0]
        dwc_xml = open("meta.xml", "w")
        dwc_xml.write('<?xml version="1.0" encoding="UTF-8"?>'
                      '\n'
                      '<SimpleDarwinRecordSet>'
                      '\n'
                      '  xmlns="http://rs.tdwg.org/dwc/xsd/simpledarwincore/"'
                      '\n'
                      '  xmlns:dc="http://purl.org/dc/terms/"'
                      '\n'
                      '  xmlns:dwc="http://rs.tdwg.org/dwc/terms/"'
                      '\n'
                      '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                      '\n'
                      '  xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">'
                      '\n'
                      )

        with open(dwc_sheet_saved, "r") as my_input_file:
            row_count = sum(1 for row in my_input_file)
            cell_value = pd.read_csv(dwc_sheet_saved)
            i = 0
            while i < row_count - 1:
                aux = 0
                dwc_xml.write('  <SimpleDarwinRecord>'
                              '\n')
                for title in dwc_titles:
                    if title in data:
                        cell = cell_value.values[i][aux]
                        dwc_xml.write(f'    <dwc:{title}>{cell}<dwc:{title}>\n')
                        aux += 1
                i += 1
                dwc_xml.write('  </SimpleDarwinRecord>'
                              '\n')

    my_input_file.close()

    dwc_xml.write('</SimpleDarwinRecordSet>')
    dwc_xml.close()
    zip = ZipFile('dwc.zip', 'w')
    zip.write(dwc_sheet_saved)
    zip.write("meta.xml")
    zip.write(txt_file)
    zip.close()
    os.remove(dwc_sheet_saved)
    os.remove("meta.xml")
    os.remove(txt_file)
    return res
