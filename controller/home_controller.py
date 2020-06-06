from flask import render_template, request, Blueprint, make_response
from model.sheet_treatment import Sheet
from werkzeug.utils import secure_filename
import pandas as pd
used_sheet = Sheet()
base_sheet = Sheet()


home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if(used_sheet.get_Path() == None):
            isUseCookie = request.cookies.get('isUseCookie')
            return render_template("index.html", isUseCookie=isUseCookie)
        else:
            return  render_template("transition/choose_route.html")
    if request.method == "POST":
        f = request.files['file']
        name_file = f.filename

        try:
            f.save("files/"+secure_filename(name_file))
            if ".csv" in name_file:
                file_csv = pd.read_csv("files/"+name_file, encoding="utf-8")
                name_file = name_file.replace(".csv", ".xls")
                file_csv.to_excel("files/"+name_file, encoding='utf-8', index=False)
                used_sheet.set_isCSV(True)
            used_sheet.set_Path_configure_all(secure_filename(name_file))
            res = make_response(render_template("transition/choose_route.html"))
            return res
        except:
            return render_template("errorscreen/InvalidFile.html")