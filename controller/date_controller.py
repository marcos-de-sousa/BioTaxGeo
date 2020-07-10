from flask import render_template, request, Blueprint, redirect, url_for, make_response
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet
from model.date import Date
date_blueprint = Blueprint('date', __name__, template_folder='templates')
date = Date()

@date_blueprint.route("/date_validation", methods=["post"])
def date_validation():
    res = make_response(redirect(url_for("home.home")))
    form = request.form.to_dict()
    list_date = used_sheet.Value_in_Column(form['column_date'])
    res.set_cookie("titles_date", form['column_date'])
    list_new_date = []
    separator = date.get_Date_Separator(form['type'])
    current_format = form['current_format']
    new_type = form['type'].split(separator)
    new_type = new_type[0]+new_type[1]+new_type[2]
    list_index_wrong_cell = []
    count = 1
    if new_type == "ddmmaaaa":
        for d in list_date:
            new_date = date.toDDMMAAAA(d, separator, current_format)
            if new_date["day"] or new_date["month"]:
                list_index_wrong_cell.append(count)
            list_new_date.append(new_date['date'])
            count+=1
    if new_type == "mmddaaaa":
        for d in list_date:
            new_date = date.toMMDDAAAA(d, separator, current_format)
            if new_date["day"] or new_date["month"]:
                list_index_wrong_cell.append(count)
            list_new_date.append(new_date['date'])
            count += 1
    if list_index_wrong_cell == []:
        list_index_wrong_cell = None
    used_sheet.Change_Column(form['column_date'], list_new_date, list_index_wrong_cell)
    used_sheet.Save_Formatted_Spreadsheet(".xls")
    return res

