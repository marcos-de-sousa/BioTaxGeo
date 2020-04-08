from flask import render_template, redirect, url_for, request, Blueprint, make_response
from controller import home_controller, form_controller
from model.data_treatment import Data_Treatment
import json

Check_Data = Data_Treatment()

used_sheet = home_controller.used_sheet

taxon_blueprint = Blueprint("taxon", __name__, template_folder="templates")


@taxon_blueprint.route("/taxon_list", methods=["GET", "POST"])
def taxon_list():
    if request.method == "POST":
        try:
            if(request.cookies.get("isUseCookie") == "accept"):
                titles_gbif = request.cookies.get("titles_gbif")
                if(titles_gbif == ""):
                    titles_gbif = None
                if(titles_gbif == None):
                    titles = request.form["selection"]
                    if ("null" in titles):
                        titles = titles.replace("null", "None")
                    titles_cookie = titles
                    titles = eval(titles)
                    used_sheet.set_Check_Columns(titles)
                    used_sheet.data_treatment.Verified_Hierarchy(used_sheet.get_Columns_Checked())
                    verification = json.dumps(used_sheet.data_treatment.get_Verified_Hierarchy())
                    response = make_response(render_template("list/taxon_list_gbif.html", verification=verification,
                                                         total_rows=used_sheet.get_Row_Total()))
                    response.set_cookie("titles_gbif", titles_cookie)
                    return response
            else:
                titles = request.form["selection"]
                if ("null" in titles):
                    titles = titles.replace("null", "None")
                titles = eval(titles)
                used_sheet.set_Check_Columns(titles)
                used_sheet.data_treatment.Verified_Hierarchy(used_sheet.get_Columns_Checked())
                verification = json.dumps(used_sheet.data_treatment.get_Verified_Hierarchy())
                return render_template("list/taxon_list_gbif.html", verification=verification,
                                                         total_rows=used_sheet.get_Row_Total())

        except:
            return render_template("errorscreen/InvalidValue.html")
    else:
        titles_cookie = request.cookies.get("titles_gbif")
        print(titles_cookie)
        titles = eval(titles_cookie)
        used_sheet.set_Check_Columns(titles)
        used_sheet.data_treatment.Verified_Hierarchy(used_sheet.get_Columns_Checked())
        verification = json.dumps(used_sheet.data_treatment.get_Verified_Hierarchy())
        response = make_response(render_template("list/taxon_list_gbif.html", verification=verification,
                                                total_rows=used_sheet.get_Row_Total()))
        response.set_cookie("titles_gbif", titles_cookie)
        return response

@taxon_blueprint.route("/taxon_validation", methods=["GET", "POST"])
def taxon_validation():
    if request.method == "POST":
        data = request.form["data"]
        data = eval(data)
        used_sheet.Change_Data_Spreadsheet(data)
        used_sheet.Save_Formatted_Spreadsheet()
        return redirect(url_for("home.home"))


@taxon_blueprint.route("/taxon_list2", methods=["GET", "POST"])
def taxon_list2():
    if request.method == "POST":
        try:
            reference_sheet = form_controller.reference_sheet
            titles_check = request.form["selection_check"]
            titles_reference = request.form["selection_base"]
            selecteds_subs = request.form["subs"]
            if ("null" in titles_check):
                titles_check = titles_check.replace("null", "None")
            if ("null" in titles_reference):
                titles_reference = titles_reference.replace("null", "None")
            titles_check = eval(titles_check)
            titles_reference = eval(titles_reference)
            selecteds_subs = eval(selecteds_subs)
            titles_cookie = {"check": titles_check, "base": titles_reference, "subs": selecteds_subs}
            titles_cookie = json.dumps(titles_cookie)

            reference_kingdom = reference_sheet.Value_in_Column(titles_reference["kingdom"]) if titles_reference["kingdom"] != "None" else None
            reference_phylum = reference_sheet.Value_in_Column(titles_reference["phylum"]) if titles_reference["phylum"] != "None" else None
            reference_class = reference_sheet.Value_in_Column(titles_reference["class"]) if titles_reference["class"] != "None" else None
            reference_order = reference_sheet.Value_in_Column(titles_reference["order"]) if titles_reference["order"] != "None" else None
            reference_family = reference_sheet.Value_in_Column(titles_reference["family"]) if titles_reference["family"] != "None" else None
            reference_genus = reference_sheet.Value_in_Column(titles_reference["genus"])
            reference_specie = reference_sheet.Value_in_Column(titles_reference["specie"])
            reference_subfamily = reference_sheet.Value_in_Column(titles_reference["subfamily"]) if titles_reference[
                                                                                                        "subfamily"] != "None" else None
            reference_subgenus = reference_sheet.Value_in_Column(titles_reference["subgenus"]) if titles_reference[
                                                                                                      "subgenus"] != "None" else None
            reference_subspecie = reference_sheet.Value_in_Column(titles_reference["subspecie"]) if titles_reference[
                                                                                                        "subspecie"] != "None" else None

            check_kingdom = used_sheet.Value_in_Column(titles_check["kingdom"]) if titles_check["kingdom"] != "None" else None
            check_phylum = used_sheet.Value_in_Column(titles_check["phylum"]) if titles_check["phylum"] != "None" else None
            check_class = used_sheet.Value_in_Column(titles_check["class"]) if titles_check["class"] != "None" else None
            check_order = used_sheet.Value_in_Column(titles_check["order"]) if titles_check["order"] != "None" else None
            check_family = used_sheet.Value_in_Column(titles_check["family"]) if titles_check["family"] != "None" else None
            check_genus = used_sheet.Value_in_Column(titles_check["genus"])
            check_specie = used_sheet.Value_in_Column(titles_check["specie"])
            check_subfamily = used_sheet.Value_in_Column(titles_check["subfamily"]) if titles_check[
                                                                                           "subfamily"] != "None" else None
            check_subgenus = used_sheet.Value_in_Column(titles_check["subgenus"]) if titles_check[
                                                                                         "subgenus"] != "None" else None
            check_subspecie = used_sheet.Value_in_Column(titles_check["subspecie"]) if titles_check[
                                                                                           "subspecie"] != "None" else None
            reference_classification_taxon = {}
            for x in range(len(reference_specie)):
                scientific_name = "{} {}".format(reference_genus[x], reference_specie[x])
                if scientific_name not in reference_classification_taxon:
                    reference_classification_taxon[scientific_name] = {
                        "genus": reference_genus[x],
                        "specie": reference_specie[x]
                    }
                    if reference_kingdom is not None:
                        reference_classification_taxon[scientific_name]["kingdom"] = reference_kingdom[x]
                    if reference_phylum is not None:
                        reference_classification_taxon[scientific_name]["phylum"] = reference_phylum[x]
                    if reference_class is not None:
                        reference_classification_taxon[scientific_name]["class"] = reference_class[x]
                    if reference_order is not None:
                        reference_classification_taxon[scientific_name]["order"] = reference_order[x]
                    if reference_family is not None:
                        reference_classification_taxon[scientific_name]["family"] = reference_family[x]
                    if reference_subfamily is not None:
                        reference_classification_taxon[scientific_name]["subfamily"] = reference_subfamily[x]
                    if reference_subgenus is not None:
                        reference_classification_taxon[scientific_name]["subgenus"] = reference_subgenus[x]
                    if reference_subspecie is not None:
                        reference_classification_taxon[scientific_name]["subspecie"] = reference_subspecie[x]
            check_classification_taxon = {}
            for x in range(len(check_specie)):
                scientific_name = "{} {}".format(check_genus[x], check_specie[x])
                if scientific_name not in check_classification_taxon:
                    check_classification_taxon[scientific_name] = {
                        "genus": check_genus[x],
                        "specie": check_specie[x]
                    }
                    if check_kingdom is not None:
                        check_classification_taxon[scientific_name]["kingdom"] = check_kingdom[x]
                    if check_phylum is not None:
                        check_classification_taxon[scientific_name]["phylum"] = check_phylum[x]
                    if check_class is not None:
                        check_classification_taxon[scientific_name]["class"] = check_class[x]
                    if check_order is not None:
                        check_classification_taxon[scientific_name]["order"] = check_order[x]
                    if check_family is not None:
                        check_classification_taxon[scientific_name]["family"] = check_family[x]
                    if check_subfamily is not None:
                        check_classification_taxon[scientific_name]["subfamily"] = check_subfamily[x]
                    if check_subgenus is not None:
                        check_classification_taxon[scientific_name]["subgenus"] = check_subgenus[x]
                    if check_subspecie is not None:
                        check_classification_taxon[scientific_name]["subspecie"] = check_subspecie[x]
            Fuzzy_Find = {}
            for specie in check_classification_taxon:
                sn_score = Check_Data.String_Similarity_2(specie, reference_classification_taxon.keys())

                def Same(a):
                    if a[1] > 60:
                        return a

                sn_score = list(filter(Same, sn_score))

                if len(sn_score) > 0:
                    key = sn_score[0][0]
                    hierarchy_score = {
                        "genus_score": "FUZZY",
                        "specie_score": "FUZZY"
                    }

                    hierarchy_suggest = {
                        "genus_suggest": [],
                        "specie_suggest": []
                    }
                    if check_kingdom is not None:
                        hierarchy_score["kingdom_score"] = "FUZZY"
                        hierarchy_suggest["kingdom_suggest"] = []
                    if check_phylum is not None:
                        hierarchy_score["phylum_score"] = "FUZZY"
                        hierarchy_suggest["phylum_suggest"] = []
                    if check_class is not None:
                        hierarchy_score["class_score"] = "FUZZY"
                        hierarchy_suggest["class_suggest"] = []
                    if check_order is not None:
                        hierarchy_score["order_score"] = "FUZZY"
                        hierarchy_suggest["order_suggest"] = []
                    if check_family is not None:
                        hierarchy_score["family_score"] = "FUZZY"
                        hierarchy_suggest["family_suggest"] = []
                    if check_subfamily is not None:
                        hierarchy_score["subfamily_score"] = "FUZZY"
                        hierarchy_suggest["subfamily_suggest"] = []
                    if check_subgenus is not None:
                        hierarchy_score["subgenus_score"] = "FUZZY"
                        hierarchy_suggest["subgenus_suggest"] = []
                    if check_subspecie is not None:
                        hierarchy_score["subspecie_score"] = "FUZZY"
                        hierarchy_suggest["subspecie_suggest"] = []

                    for i in sn_score:
                        for key in check_classification_taxon[specie]:
                            if check_classification_taxon[specie][key] == reference_classification_taxon[i[0]][key]:
                                hierarchy_score[key + "_score"] = "EXACT"
                            else:
                                hierarchy_suggest[key + "_suggest"].append(reference_classification_taxon[i[0]][key])

                    Fuzzy_Find[specie] = {}
                    if check_kingdom is not None:
                        Fuzzy_Find[specie]["kingdom"] = {
                            "amount": check_kingdom.count(check_classification_taxon[specie]["kingdom"]),
                            "correctness": hierarchy_score["kingdom_score"],
                            "suggestion": hierarchy_suggest["kingdom_suggest"],
                            "title": titles_check["kingdom"],
                            "type": check_classification_taxon[specie]["kingdom"]
                        }
                    if check_phylum is not None:
                        Fuzzy_Find[specie]["phylum"] = {
                            "amount": check_phylum.count(check_classification_taxon[specie]["phylum"]),
                            "correctness": hierarchy_score["phylum_score"],
                            "suggestion": hierarchy_suggest["phylum_suggest"],
                            "title": titles_check["phylum"],
                            "type": check_classification_taxon[specie]["phylum"]
                        }
                    if check_class is not None:
                        Fuzzy_Find[specie]["class"] = {
                            "amount": check_class.count(check_classification_taxon[specie]["class"]),
                            "correctness": hierarchy_score["class_score"],
                            "suggestion": hierarchy_suggest["class_suggest"],
                            "title": titles_check["class"],
                            "type": check_classification_taxon[specie]["class"]
                        }
                    if check_order is not None:
                        Fuzzy_Find[specie]["order"] = {
                            "amount": check_order.count(check_classification_taxon[specie]["order"]),
                            "correctness": hierarchy_score["order_score"],
                            "suggestion": hierarchy_suggest["order_suggest"],
                            "title": titles_check["order"],
                            "type": check_classification_taxon[specie]["order"]
                        }
                    if check_family is not None:
                        Fuzzy_Find[specie]["family"] = {
                            "amount": check_family.count(check_classification_taxon[specie]["family"]),
                            "correctness": hierarchy_score["family_score"],
                            "suggestion": hierarchy_suggest["family_suggest"],
                            "title": titles_check["family"],
                            "type": check_classification_taxon[specie]["family"]
                        }
                    if check_subfamily is not None:
                        Fuzzy_Find[specie]["subfamily"] = {
                            "amount": check_subfamily.count(check_classification_taxon[specie]["subfamily"]),
                            "correctness": hierarchy_score["subfamily_score"],
                            "suggestion": hierarchy_suggest["subfamily_suggest"],
                            "title": titles_check["subfamily"],
                            "type": check_classification_taxon[specie]["subfamily"]
                        }
                    Fuzzy_Find[specie]["genus"] = {
                        "amount": check_genus.count(check_classification_taxon[specie]["genus"]),
                        "correctness": hierarchy_score["genus_score"],
                        "suggestion": hierarchy_suggest["genus_suggest"],
                        "title": titles_check["genus"],
                        "type": check_classification_taxon[specie]["genus"]
                    }
                    if check_subgenus is not None:
                        Fuzzy_Find[specie]["subgenus"] = {
                            "amount": check_subgenus.count(check_classification_taxon[specie]["subgenus"]),
                            "correctness": hierarchy_score["subgenus_score"],
                            "suggestion": hierarchy_suggest["subgenus_suggest"],
                            "title": titles_check["subgenus"],
                            "type": check_classification_taxon[specie]["subgenus"]
                        }
                    Fuzzy_Find[specie]["specie"] = {
                        "amount": check_specie.count(check_classification_taxon[specie]["specie"]),
                        "correctness": hierarchy_score["specie_score"],
                        "suggestion": hierarchy_suggest["specie_suggest"],
                        "title": titles_check["specie"],
                        "type": check_classification_taxon[specie]["specie"]
                    }
                    if check_subspecie is not None:
                        Fuzzy_Find[specie]["subspecie"] = {
                            "amount": check_subspecie.count(check_classification_taxon[specie]["subspecie"]),
                            "correctness": hierarchy_score["subspecie_score"],
                            "suggestion": hierarchy_suggest["subspecie_suggest"],
                            "title": titles_check["subspecie"],
                            "type": check_classification_taxon[specie]["subspecie"]
                        }
                    Fuzzy_Find[specie]["scientific name"] = {
                        "correctness": "EXACT",
                        "font": "Planilha",
                        "suggestion": "NONE",
                        "synonymous": "false",
                        "type": specie
                    }
                else:
                    hierarchy_score = {
                        "kingdom_score": "Not found",
                        "phylum_score": "Not found",
                        "class_score": "Not found",
                        "order_score": "Not found",
                        "family_score": "Not found",
                        "genus_score": "Not found",
                        "specie_score": "Not found",
                        "subfamily_score": "Not found",
                        "subgenus_score": "Not found",
                        "subspecie_score": "Not found"
                    }
                    precision = "Not found"

                    Fuzzy_Find[specie] = {}
                    if check_kingdom is not None:
                        Fuzzy_Find[specie]["kingdom"] = {
                            "amount": check_kingdom.count(check_classification_taxon[specie]["kingdom"]),
                            "correctness": hierarchy_score["kingdom_score"],
                            "suggestion": "",
                            "title": titles_check["kingdom"],
                            "type": check_classification_taxon[specie]["kingdom"]
                        }
                    if check_phylum is not None:
                        Fuzzy_Find[specie]["phylum"] = {
                            "amount": check_phylum.count(check_classification_taxon[specie]["phylum"]),
                            "correctness": hierarchy_score["phylum_score"],
                            "suggestion": "",
                            "title": titles_check["phylum"],
                            "type": check_classification_taxon[specie]["phylum"]
                        }
                    if check_class is not None:
                        Fuzzy_Find[specie]["class"] = {
                            "amount": check_class.count(check_classification_taxon[specie]["class"]),
                            "correctness": hierarchy_score["class_score"],
                            "suggestion": "",
                            "title": titles_check["class"],
                            "type": check_classification_taxon[specie]["class"]
                        }
                    if check_order is not None:
                        Fuzzy_Find[specie]["order"] = {
                            "amount": check_order.count(check_classification_taxon[specie]["order"]),
                            "correctness": hierarchy_score["order_score"],
                            "suggestion": "",
                            "title": titles_check["order"],
                            "type": check_classification_taxon[specie]["order"]
                        }
                    if check_family is not None:
                        Fuzzy_Find[specie]["family"] = {
                            "amount": check_family.count(check_classification_taxon[specie]["family"]),
                            "correctness": hierarchy_score["family_score"],
                            "suggestion": "",
                            "title": titles_check["family"],
                            "type": check_classification_taxon[specie]["family"]
                        }
                    if check_subfamily is not None:
                        Fuzzy_Find[specie]["subfamily"] = {
                            "amount": check_subfamily.count(check_classification_taxon[specie]["subfamily"]),
                            "correctness": hierarchy_score["subfamily_score"],
                            "suggestion": "",
                            "title": titles_check["subfamily"],
                            "type": check_classification_taxon[specie]["subfamily"]
                        }
                    Fuzzy_Find[specie]["genus"] = {
                        "amount": check_genus.count(check_classification_taxon[specie]["genus"]),
                        "correctness": hierarchy_score["genus_score"],
                        "suggestion": "",
                        "title": titles_check["genus"],
                        "type": check_classification_taxon[specie]["genus"]
                    }
                    if check_subgenus is not None:
                        Fuzzy_Find[specie]["subgenus"] = {
                            "amount": check_subgenus.count(check_classification_taxon[specie]["subgenus"]),
                            "correctness": hierarchy_score["subgenus_score"],
                            "suggestion": "",
                            "title": titles_check["subgenus"],
                            "type": check_classification_taxon[specie]["subgenus"]
                        }
                    Fuzzy_Find[specie]["specie"] = {
                        "amount": check_specie.count(check_classification_taxon[specie]["specie"]),
                        "correctness": hierarchy_score["specie_score"],
                        "suggestion": "",
                        "title": titles_check["specie"],
                        "type": check_classification_taxon[specie]["specie"]
                    }
                    if check_subspecie is not None:
                        Fuzzy_Find[specie]["subspecie"] = {
                            "amount": check_subspecie.count(check_classification_taxon[specie]["subspecie"]),
                            "correctness": hierarchy_score["subspecie_score"],
                            "suggestion": "",
                            "title": titles_check["subspecie"],
                            "type": check_classification_taxon[specie]["subspecie"]
                        }
                    Fuzzy_Find[specie]["scientific name"] = {
                        "correctness": precision,
                        "font": "Planilha",
                        "suggestion": "NONE",
                        "synonymous": "false",
                        "type": specie
                    }
            used_sheet.data_treatment.set_Verified_Hierarchy(Fuzzy_Find)
            Fuzzy_Find = json.dumps(Fuzzy_Find)

            if (request.cookies.get("isUseCookie") == "accept"):
                response = make_response(render_template("list/taxon_list_localsheet.html", verification=Fuzzy_Find,
                                                         total_rows=used_sheet.get_Row_Total()))
                response.set_cookie("titles_localsheet", titles_cookie)
                return response
            else:
                return render_template("list/taxon_list_localsheet.html", verification=Fuzzy_Find,
                                                         total_rows=used_sheet.get_Row_Total())
        except:
            return render_template("errorscreen/InvalidValue.html")
