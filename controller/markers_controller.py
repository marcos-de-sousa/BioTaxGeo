from flask import render_template, redirect, url_for, request, Blueprint, make_response
from controller import home_controller
from model.hierarchy_taxon import Hierarchy_Taxon
import googlemaps
import json

spreadsheet_titles = {}
file_api = open('googlemaps_api_key.txt', 'r')
google_key = file_api.read()
file_api.close()
gmaps = googlemaps.Client(key=google_key)
used_sheet = home_controller.used_sheet

markers_blueprint = Blueprint('markers', __name__, template_folder='templates', static_url_path="static")

@markers_blueprint .route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        titles_cookie = []
        coord = request.form["selection_coordinate"]
        coord = eval(coord)
        titles_cookie.append(coord)
        region = request.form["selection_region"]
        region = eval(region)
        titles_cookie.append(region)
        used_sheet.coordinate.set_Latitude_Column_values(coord["latitude"])
        used_sheet.coordinate.set_Longitude_Column_values(coord["longitude"])

        used_sheet.locality.set_Country_Column_values(region["country"])
        used_sheet.locality.set_State_Column_values(region["state"])
        used_sheet.locality.set_County_Column_values(region["county"])

        spreadsheet_titles['country'] = region["country"]
        spreadsheet_titles['state'] = region["state"]
        spreadsheet_titles['county'] = region["county"]
        spreadsheet_titles['latitude'] = coord["latitude"]
        spreadsheet_titles['longitude'] = coord["longitude"]
        if (request.cookies.get("isUseCookie") == "accept"):
            response = make_response(redirect(url_for("markers.markers_form_map")))
            titles_cookie = json.dumps(titles_cookie)
            response.set_cookie("titles_marker", titles_cookie)
            return response
        else:
            return redirect(url_for("markers.markers_form_map"))

@markers_blueprint .route("/markers_form_map",methods=["GET","POST"])
def markers_form_map():
    if request.method == "GET":
        return render_template("form/markers_form_map.html", google_key=google_key)

@markers_blueprint .route("/markers_list_map",methods=["GET","POST"])
def markers_list_map():
    if request.method == "GET":
        return redirect(url_for("markers.markers_form_map"))
    elif request.method == "POST":
        try:
            polygons = request.form['vertices']
            polygons = eval(polygons)
            coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
            coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
            coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
            coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)

            spreadsheet_country = used_sheet.locality.get_Country_Column_values()
            spreadsheet_state = used_sheet.locality.get_State_Column_values()
            spreadsheet_county = used_sheet.locality.get_County_Column_values()

            list_empty_values = [i for i, item in enumerate(coord_lat) if item == '']
            count = 0
            list_region = []
            list_treatment_region = []
            for x in list_empty_values:
                delete = x-count
                del(coord_lat[delete])
                del(coord_lng[delete])
                del(spreadsheet_country[delete])
                del(spreadsheet_state[delete])
                del(spreadsheet_county[delete])
                count+=1
            try:
                for x in range(len(coord_lat)):
                    region = {"country": "null", "state": "null", "county": "null"}
                    reverse_geocode_result = gmaps.reverse_geocode((coord_lat[x], coord_lng[x]), language="pt-BR")
                    index = 0
                    for x in range(len(reverse_geocode_result)):
                        if reverse_geocode_result[x]['types'][0] == 'administrative_area_level_2':
                            index = x
                    try:
                        region['country'] = reverse_geocode_result[index]['address_components'][2]['long_name']
                    except:
                        region['country'] = "null"
                    try:
                        region['state'] = reverse_geocode_result[index]['address_components'][1]['long_name']
                    except:
                        region['state'] = "null"
                    try:
                        region['county'] = reverse_geocode_result[index]['address_components'][0]['long_name']
                    except:
                        region['county'] = "null"
                    list_region.append(region)

                for x in range(len(list_region)):
                    checked_region = {"country": {'name1': None, 'name2': None, 'score': None}, "state": {'name1': None, 'name2': None, 'score': None}, "county": {'name1': None, 'name2': None, 'score': None}}
                    checked_region['country']['name1'] = spreadsheet_country[x]
                    checked_region['country']['name2'] = list_region[x]['country']
                    checked_region['country']['score'] = used_sheet.data_treatment.Compare_String(spreadsheet_country[x], list_region[x]['country'])

                    checked_region['state']['name1'] = spreadsheet_state[x]
                    checked_region['state']['name2'] = list_region[x]['state']
                    checked_region['state']['score'] = used_sheet.data_treatment.Compare_String(spreadsheet_state[x], list_region[x]['state'])

                    checked_region['county']['name1'] = spreadsheet_county[x]
                    checked_region['county']['name2'] = list_region[x]['county']
                    checked_region['county']['score'] = used_sheet.data_treatment.Compare_String(spreadsheet_county[x], list_region[x]['county'])

                    list_treatment_region.append(checked_region)
            except NameError:
                print("erro: "+NameError)
            row_coord_lat = used_sheet.coordinate.get_Index_Row_Lat()
            row_coord_lng = used_sheet.coordinate.get_Index_Row_Lng()
            return render_template("list/markers_list.html", google_key=google_key, polygons=polygons, latitude=coord_lat, longitude=coord_lng, row_coord_lat=row_coord_lat, row_coord_lng=row_coord_lng, list_region=list_region, country=spreadsheet_country, state=spreadsheet_state, county=spreadsheet_county, list_checked_regions=list_treatment_region, spreadsheet_titles=spreadsheet_titles)
        except:
            return render_template("errorscreen/InvalidValue.html")
@markers_blueprint .route("/markers_confirm", methods=["GET", "POST"])
def markers_confirm():
    if request.method == "POST":
        data = request.form["data"]
        data = eval(data)
        type = request.form["type_file"]
        used_sheet.Change_Data_Spreadsheet2(data)
        used_sheet.Save_Formatted_Spreadsheet(type)
        return redirect(url_for("home.home"))
    else:
        return redirect(url_for("home.home"))