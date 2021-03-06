from flask import render_template, redirect, url_for, request, Blueprint, make_response
from controller import home_controller
from werkzeug.utils import secure_filename
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
        format_coordinate = request.form["format_coordinate"]
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
            response.set_cookie("format_coordinate", format_coordinate)
            return response
        else:

            return redirect(url_for("markers.markers_form_map"))

@markers_blueprint .route("/markers_form_map",methods=["GET","POST"])
def markers_form_map():
    if request.method == "GET":
        return render_template("form/markers_form_map.html", google_key=google_key, geojson="null")
    else:
        f = request.files['file']
        name_file = f.filename
        f.save("files/" + secure_filename(name_file))

        return render_template("form/markers_form_map.html", google_key=google_key, geojson=name_file)

@markers_blueprint .route("/markers_list_map",methods=["GET","POST"])
def markers_list_map():
    if request.method == "GET":
        return redirect(url_for("markers.markers_form_map"))
    elif request.method == "POST":
        try:
            polygons = request.form['vertices']
            polygons = eval(polygons)
            geojson = request.form['geojson_names']
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
            for x in range(len(coord_lat)):
                region = {"country": "null", "state": "null", "county": "null"}
                if type(coord_lat[x])==float and type(coord_lng[x])==float:
                    reverse_geocode_result = gmaps.reverse_geocode((coord_lat[x], coord_lng[x]), language="pt-BR")
                else:
                    if type(coord_lat[x]) == str:
                        coord_lat[x] = 0.0
                    if type(coord_lng[x]) == str:
                        coord_lng[x] = 0.0
                    reverse_geocode_result = []
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

            row_coord_lat = used_sheet.coordinate.get_Index_Row_Lat()
            row_coord_lng = used_sheet.coordinate.get_Index_Row_Lng()
            return render_template("list/markers_list.html", geojson_names=geojson, google_key=google_key, polygons=polygons, latitude=coord_lat, longitude=coord_lng, row_coord_lat=row_coord_lat, row_coord_lng=row_coord_lng, list_region=list_region, country=spreadsheet_country, state=spreadsheet_state, county=spreadsheet_county, list_checked_regions=list_treatment_region, spreadsheet_titles=spreadsheet_titles)
        except:
            return render_template("errorscreen/InvalidValue.html")

@markers_blueprint .route("/markers_confirm", methods=["GET", "POST"])
def markers_confirm():
    if request.method == "POST":
        data = request.form["data"]
        data = eval(data)
        type = request.form["type_file"]
        titles = request.cookies.get("titles_marker")
        titles = eval(titles)
        format_coordinate = request.cookies.get("format_coordinate")
        used_sheet.Change_Data_Spreadsheet2(data)
        coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
        coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
        coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
        coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)

        if format_coordinate != "None":
            if (format_coordinate == "Decimal"):
                used_sheet.Change_Column(titles[0]["latitude"], coord_lat, name="decimal_latitude")
                used_sheet.set_Columns_Total(used_sheet.get_Columns_Total() + 1)
                used_sheet.Change_Column(titles[0]["longitude"], coord_lng, name="decimal_longitude")
                used_sheet.Save_Formatted_Spreadsheet(type)
                return redirect(url_for("home.home"))
            elif (format_coordinate == "DMS"):
                lat_ddmmss = []
                lng_ddmmss = []
                for i in range(len(coord_lat)):
                    lat_ddmmss.append(used_sheet.coordinate.toDDMMSS(coord_lat[i], "lat"))
                    lng_ddmmss.append(used_sheet.coordinate.toDDMMSS(coord_lng[i], "lng"))
                used_sheet.Change_Column(titles[0]["latitude"], lat_ddmmss, name="DDMMSS_latitude")
                used_sheet.set_Columns_Total(used_sheet.get_Columns_Total() + 1)
                used_sheet.Change_Column(titles[0]["longitude"], lng_ddmmss, name="DDMMSS_longitude")
                used_sheet.Save_Formatted_Spreadsheet(type)
                return redirect(url_for("home.home"))
            elif (format_coordinate == "DM"):
                lat_ddmm = []
                lng_ddmm = []
                for i in range(len(coord_lat)):
                    lat_ddmm.append(used_sheet.coordinate.toDDMM(coord_lat[i], "lat"))
                    lng_ddmm.append(used_sheet.coordinate.toDDMM(coord_lng[i], "lng"))
                used_sheet.Change_Column(titles[0]["latitude"], lat_ddmm, name="DDMM_latitude")
                used_sheet.set_Columns_Total(used_sheet.get_Columns_Total() + 1)
                used_sheet.Change_Column(titles[0]["longitude"], lng_ddmm, name="DDMM_longitude")
                used_sheet.Save_Formatted_Spreadsheet(type)
                return redirect(url_for("home.home"))

        used_sheet.Save_Formatted_Spreadsheet(type)
        return redirect(url_for("home.home"))
    else:
        return redirect(url_for("home.home"))