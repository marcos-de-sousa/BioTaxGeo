from flask import render_template, request, Blueprint, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from model.sheet_treatment import Sheet
from controller.home_controller import used_sheet

reference_sheet = Sheet()

form_blueprint = Blueprint('form', __name__, template_folder='templates')


@form_blueprint.route("/taxon_form", methods=["GET", "POST"])
def taxon_form():
    if request.method == 'GET':
        titles_cookie = request.cookies.get("titles_gbif")
        if titles_cookie == "":
            titles_cookie = None
        if(request.cookies.get("isUseCookie") == "accept"):
            if(titles_cookie != None):
                return redirect(url_for("taxon.taxon_list"))
            else:
                return render_template("form/taxon_form_gbif.html", titles=used_sheet.get_Sheet_Header(), cookies = titles_cookie)
        else:
            return render_template("form/taxon_form_gbif.html", titles=used_sheet.get_Sheet_Header(), cookies = titles_cookie)
    else:
        res = make_response(render_template("form/taxon_form_gbif.html", titles=used_sheet.get_Sheet_Header()))
        res.set_cookie("titles_gbif", "None")
        return redirect(url_for("form.taxon_form"))
@form_blueprint.route("/taxon_form2", methods=["GET", "POST"])
def taxon_form2():
    if request.method == 'POST':
        try:
            f = request.files['file']
            f.save("files/"+secure_filename(f.filename))
            reference_sheet.set_Path_configure_all(secure_filename(f.filename))
            titles_cookie = request.cookies.get("titles_localsheet")
            return render_template("form/taxon_form_localsheet.html", titles_check=used_sheet.get_Sheet_Header(), titles_base=reference_sheet.get_Sheet_Header(), cookies = titles_cookie)
        except:
            reference_sheet.set_Path(None)
            return render_template("errorscreen/InvalidFile.html")
    else:
        return redirect(url_for("home.home"))

@form_blueprint.route("/markers_form", methods=["GET", "POST"])
def markers_form():
    if request.method == 'GET':
        cookies = request.cookies.get("titles_marker")
        return render_template("form/markers_form.html", titles=used_sheet.get_Sheet_Header(), cookies=cookies)
