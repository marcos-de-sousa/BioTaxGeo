import requests
from model.taxon_validation import Taxon_Validation
from fuzzywuzzy import fuzz, process

class Data_Treatment:

    def __init__(self, sht=None):
        self.verified_hierarchy = {}  # NC = Nomes Científicos
        self.validate_columns = {}
        self.sheet = sht
        self.original_titles = []
        self.taxon_validation = None

    def set_Check_Columns (self, title, value):
        self.validate_columns[title] = value

    def set_Original_Titles (self, title):
        self.original_titles.append(title)
    def Reset_Values(self):
        self.verified_hierarchy = {}  # NC = Nomes Científicos
        self.validate_columns = {}
        self.original_titles = []
        self.taxon_validation = None
    def get_Original_Titles (self):
        return self.original_titles

    def get_Validate_Columns (self):
        if not self.validate_columns:
            return "Empty list"
        else:
            return self.validate_columns

    def Verified_Hierarchy (self, hierarchy):
        check_hrch = hierarchy
        for index in range(0, len(check_hrch["specie"])):
            if (check_hrch["genus"][index] != ""):
                Scientific_Name = check_hrch["genus"][index] + " " + check_hrch["specie"][index]

                self.taxon_validation = Taxon_Validation(
                                                         k=check_hrch['kingdom'][index],
                                                         p=check_hrch['phylum'] [index],
                                                         c=check_hrch['class'] [index],
                                                         o=check_hrch['order']  [index],
                                                         f=check_hrch['family'][index],
                                                         g=check_hrch['genus'] [index],
                                                         e=check_hrch['specie'] [index],
                                                         sn=Scientific_Name
                                                        )

                if Scientific_Name in self.verified_hierarchy:
                    continue
                else:
                    gbif_values = requests.get(
                        'http://api.gbif.org/v1/species/match?name=' + Scientific_Name + "&rank=SPECIES&strict=true").json()
                    if (gbif_values["matchType"] != "NONE"):

                        self.taxon_validation.set_Hierarchy_Correctness(
                                                                        gbif_values["kingdom"],
                                                                        gbif_values["phylum"] ,
                                                                        gbif_values["class"]  ,
                                                                        gbif_values["order"]  ,
                                                                        gbif_values["family"] ,
                                                                        gbif_values["genus"]  ,
                                                                        gbif_values["species"],
                                                                        gbif_values["canonicalName"]
                                                                       )

                        self.taxon_validation.set_Hierarchy_Suggestion(
                                                                       gbif_values["kingdom"],
                                                                       gbif_values["phylum"] ,
                                                                       gbif_values["class"]  ,
                                                                       gbif_values["order"]  ,
                                                                       gbif_values["family"] ,
                                                                       gbif_values["genus"]  ,
                                                                       gbif_values["species"],
                                                                       gbif_values["canonicalName"]
                                                                      )

                        self.verified_hierarchy[Scientific_Name] = {
                            "kingdom": {
                                "type": self.taxon_validation.get_Kingdom(),
                                "correctness": self.taxon_validation.get_Kingdom_Correctness(),
                                "amount": check_hrch['kingdom'].count(self.taxon_validation.get_Kingdom()),
                                "suggestion": self.taxon_validation.get_Kingdom_Suggestion(),
                                "title": self.get_Original_Titles()[0]

                            },
                            "phylum": {
                                "type": self.taxon_validation.get_Phylum(),
                                "correctness": self.taxon_validation.get_Phylum_Correctness(),
                                "amount": check_hrch['phylum'].count(self.taxon_validation.get_Phylum()),
                                "suggestion": self.taxon_validation.get_Phylum_Suggestion(),
                                "title": self.get_Original_Titles()[1]
                            },
                            "class": {
                                "type": self.taxon_validation.get_Classs(),
                                "correctness": self.taxon_validation.get_Classs_Correctness(),
                                "amount": check_hrch['class'].count(self.taxon_validation.get_Classs()),
                                "suggestion": self.taxon_validation.get_Classs_Suggestion(),
                                "title": self.get_Original_Titles()[2]
                            },
                            "order": {
                                "type": self.taxon_validation.get_Order(),
                                "correctness": self.taxon_validation.get_Order_Correctness(),
                                "amount": check_hrch['order'].count(self.taxon_validation.get_Order()),
                                "suggestion": self.taxon_validation.get_Order_Suggestion(),
                                "title": self.get_Original_Titles()[3]
                            },
                            "family": {
                                "type": self.taxon_validation.get_Family(),
                                "correctness": self.taxon_validation.get_Family_Correctness(),
                                "amount": check_hrch['family'].count(self.taxon_validation.get_Family()),
                                "suggestion": self.taxon_validation.get_Family_Suggestion(),
                                "title": self.get_Original_Titles()[4]
                            },
                            "genus": {
                                "type": self.taxon_validation.get_Genus(),
                                "correctness": self.taxon_validation.get_Genus_Correctness(),
                                "amount": check_hrch['genus'].count(self.taxon_validation.get_Genus()),
                                "suggestion": self.taxon_validation.get_Genus_Suggestion(),
                                "title": self.get_Original_Titles()[5]
                            },
                            "specie": {
                                "type": self.taxon_validation.get_Specie(),
                                "correctness": self.taxon_validation.get_Specie_Correctness(),
                                "amount": check_hrch['specie'].count(self.taxon_validation.get_Specie()),
                                "suggestion": self.taxon_validation.get_Specie_Suggestion(),
                                "title": self.get_Original_Titles()[6]
                            },
                            "scientific name": {
                                "type": self.taxon_validation.get_Scientific_Name(),
                                "correctness": self.taxon_validation.get_Scientific_Name_Correctness(),
                                "suggestion": self.taxon_validation.get_Scientific_Name_Suggestion(),
                                "synonymous": gbif_values["synonym"],
                                "font": "GBIF",
                                "synonym": gbif_values["usageKey"],
                                "accept": gbif_values["speciesKey"],
                                "canonicalname": gbif_values["canonicalName"],
                                "speciesname": gbif_values["species"]
                            }
                        }
                    else:
                        self.verified_hierarchy[Scientific_Name] = {
                            "kingdom": {
                                "type": self.taxon_validation.get_Kingdom(),
                                "correctness": self.taxon_validation.get_Kingdom_Correctness(),
                                "amount": check_hrch['kingdom'].count(self.taxon_validation.get_Kingdom()),
                                "suggestion": self.taxon_validation.get_Kingdom_Suggestion(),
                                "title": self.get_Original_Titles()[0]
                            },
                            "phylum": {
                                "type": self.taxon_validation.get_Phylum(),
                                "correctness": self.taxon_validation.get_Phylum_Correctness(),
                                "amount": check_hrch['phylum'].count(self.taxon_validation.get_Phylum()),
                                "suggestion": self.taxon_validation.get_Phylum_Suggestion(),
                                "title": self.get_Original_Titles()[1]
                            },
                            "class": {
                                "type": self.taxon_validation.get_Classs(),
                                "correctness": self.taxon_validation.get_Classs_Correctness(),
                                "amount": check_hrch['class'].count(self.taxon_validation.get_Classs()),
                                "suggestion": self.taxon_validation.get_Classs_Suggestion(),
                                "title": self.get_Original_Titles()[2]
                            },
                            "order": {
                                "type": self.taxon_validation.get_Order(),
                                "correctness": self.taxon_validation.get_Order_Correctness(),
                                "amount": check_hrch['order'].count(self.taxon_validation.get_Order()),
                                "suggestion": self.taxon_validation.get_Order_Suggestion(),
                                "title": self.get_Original_Titles()[3]
                            },
                            "family": {
                                "type": self.taxon_validation.get_Family(),
                                "correctness": self.taxon_validation.get_Family_Correctness(),
                                "amount": check_hrch['family'].count(self.taxon_validation.get_Family()),
                                "suggestion": self.taxon_validation.get_Family_Suggestion(),
                                "title": self.get_Original_Titles()[4]
                            },
                            "genus": {
                                "type": self.taxon_validation.get_Genus(),
                                "correctness": self.taxon_validation.get_Genus_Correctness(),
                                "amount": check_hrch['genus'].count(self.taxon_validation.get_Genus()),
                                "suggestion": self.taxon_validation.get_Genus_Suggestion(),
                                "title": self.get_Original_Titles()[5]
                            },
                            "specie": {
                                "type": self.taxon_validation.get_Specie(),
                                "correctness": self.taxon_validation.get_Specie_Correctness(),
                                "amount": check_hrch['specie'].count(self.taxon_validation.get_Specie()),
                                "suggestion": self.taxon_validation.get_Specie_Suggestion(),
                                "title": self.get_Original_Titles()[6]
                            },
                            "scientific name": {
                                "type": self.taxon_validation.get_Scientific_Name(),
                                "correctness": self.taxon_validation.get_Scientific_Name_Correctness(),
                                "suggestion": self.taxon_validation.get_Scientific_Name_Suggestion(),
                                "synonymous": "",
                                "font": "Planilha",
                                "synonym": "",
                                "accept": "",
                                "canonicalname": "",
                                "speciesname": ""
                            }
                        }
        for wrong_name in self.verified_hierarchy:
            if self.verified_hierarchy[wrong_name]["scientific name"]["correctness"] == "NONE":
                gbif_suggest = requests.get('http://api.gbif.org/v1/species/suggest?q=' + wrong_name + '&rank=SPECIES&strict=true').json()
                if not gbif_suggest:
                    average_hierarchy_values = {}
                    for correct_name in self.verified_hierarchy:
                        average_hierarchy_values[correct_name] = {}
                        for key in self.verified_hierarchy[correct_name]:
                            average_hierarchy_values[correct_name][key] = {}
                            if self.verified_hierarchy[correct_name][key]["correctness"] == "EXACT" and key != "scientific name":
                                correct = self.verified_hierarchy[correct_name][key]["type"]
                                wrong = self.verified_hierarchy[wrong_name][key]["type"]
                                average_hierarchy_values[correct_name][key][correct] = None

                                if (self.Compare_String (wrong, correct) > 60 and wrong != correct):
                                    if correct not in self.verified_hierarchy[wrong_name][key]["suggestion"]:
                                        self.verified_hierarchy[wrong_name][key]["suggestion"].append(correct)
                                    self.verified_hierarchy[wrong_name]["scientific name"]["font"] = "Planilha"

                                if (correct == wrong):
                                    self.verified_hierarchy[wrong_name][key]["correctness"] = self.verified_hierarchy[correct_name][key]["correctness"]

                else:
                    self.taxon_validation = Taxon_Validation(
                        k=self.verified_hierarchy[wrong_name]["kingdom"]["type"],
                        p=self.verified_hierarchy[wrong_name]["phylum"]["type"],
                        c=self.verified_hierarchy[wrong_name]["class"]["type"],
                        o=self.verified_hierarchy[wrong_name]["order"]["type"],
                        f=self.verified_hierarchy[wrong_name]["family"]["type"],
                        g=self.verified_hierarchy[wrong_name]["genus"]["type"],
                        e=self.verified_hierarchy[wrong_name]["scientific name"]["type"],
                        sn=self.verified_hierarchy[wrong_name]["scientific name"]["type"]
                    )
                    for key in self.verified_hierarchy[wrong_name]:
                        self.verified_hierarchy[wrong_name][key]["suggestion"] = []
                    for index in range(0, len(gbif_suggest)):
                        try:

                            self.taxon_validation.set_Hierarchy_Correctness(
                                                                            gbif_suggest[index]["kingdom"],
                                                                            gbif_suggest[index]["phylum"] ,
                                                                            gbif_suggest[index]["class"]  ,
                                                                            gbif_suggest[index]["order"]  ,
                                                                            gbif_suggest[index]["family"] , 
                                                                            gbif_suggest[index]["genus"]  ,
                                                                            gbif_suggest[index]["species"], 
                                                                            gbif_suggest[index]["canonicalName"]
                                                                           )

                            self.taxon_validation.set_Hierarchy_Suggestion(
                                                                           gbif_suggest[index]["kingdom"], 
                                                                           gbif_suggest[index]["phylum"] ,
                                                                           gbif_suggest[index]["class"]  , 
                                                                           gbif_suggest[index]["order"]  ,
                                                                           gbif_suggest[index]["family"] , 
                                                                           gbif_suggest[index]["genus"]  ,
                                                                           gbif_suggest[index]["species"], 
                                                                           gbif_suggest[index]["canonicalName"]
                                                                          )

                        except:
                            print('http://api.gbif.org/v1/species/suggest?q=' + wrong_name + '&rank=SPECIES&strict=true')
                        self.verified_hierarchy[wrong_name]["kingdom"]["suggestion"].append(
                            self.taxon_validation.get_Kingdom_Suggestion()) if self.taxon_validation.get_Kingdom_Suggestion() not in \
                                                                                 self.verified_hierarchy[
                                                                                     wrong_name]["kingdom"][
                                                                                     "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["phylum"]["suggestion"].append(
                            self.taxon_validation.get_Phylum_Suggestion()) if self.taxon_validation.get_Phylum_Suggestion() not in \
                                                                                self.verified_hierarchy[wrong_name][
                                                                                    "phylum"]["suggestion"] else None
                        self.verified_hierarchy[wrong_name]["class"]["suggestion"].append(
                            self.taxon_validation.get_Classs_Suggestion()) if self.taxon_validation.get_Classs_Suggestion() not in \
                                                                                  self.verified_hierarchy[
                                                                                      wrong_name]["class"][
                                                                                      "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["order"]["suggestion"].append(
                            self.taxon_validation.get_Order_Suggestion()) if self.taxon_validation.get_Order_Suggestion() not in \
                                                                                 self.verified_hierarchy[
                                                                                     wrong_name]["order"][
                                                                                     "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["family"]["suggestion"].append(
                            self.taxon_validation.get_Family_Suggestion()) if self.taxon_validation.get_Family_Suggestion() not in \
                                                                                   self.verified_hierarchy[
                                                                                       wrong_name]["family"][
                                                                                       "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["genus"]["suggestion"].append(
                            self.taxon_validation.get_Genus_Suggestion()) if self.taxon_validation.get_Genus_Suggestion() not in \
                                                                                  self.verified_hierarchy[
                                                                                      wrong_name]["genus"][
                                                                                      "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["specie"]["suggestion"].append(
                            self.taxon_validation.get_Specie_Suggestion()) if self.taxon_validation.get_Specie_Suggestion() not in \
                                                                                   self.verified_hierarchy[
                                                                                       wrong_name]["specie"][
                                                                                       "suggestion"] else None
                        self.verified_hierarchy[wrong_name]["scientific name"]["suggestion"].append(
                            self.taxon_validation.get_Scientific_Name_Suggestion()) if self.taxon_validation.get_Scientific_Name_Suggestion() not in \
                                                                                           self.verified_hierarchy[
                                                                                               wrong_name][
                                                                                               "scientific name"][
                                                                                               "suggestion"] else None

                        self.verified_hierarchy[wrong_name]["kingdom"][
                            "correctness"] = self.taxon_validation.get_Kingdom_Correctness()
                        self.verified_hierarchy[wrong_name]["phylum"][
                            "correctness"] = self.taxon_validation.get_Phylum_Correctness()
                        self.verified_hierarchy[wrong_name]["class"][
                            "correctness"] = self.taxon_validation.get_Classs_Correctness()
                        self.verified_hierarchy[wrong_name]["order"][
                            "correctness"] = self.taxon_validation.get_Order_Correctness()
                        self.verified_hierarchy[wrong_name]["family"][
                            "correctness"] = self.taxon_validation.get_Family_Correctness()
                        self.verified_hierarchy[wrong_name]["genus"][
                            "correctness"] = self.taxon_validation.get_Genus_Correctness()
                        self.verified_hierarchy[wrong_name]["specie"][
                            "correctness"] = self.taxon_validation.get_Specie_Correctness()
                        
                        self.verified_hierarchy[wrong_name]["scientific name"]["correctness"] = self.taxon_validation.get_Scientific_Name_Correctness()
                        self.verified_hierarchy[wrong_name]["scientific name"]["font"] = "GBIF"
                        self.verified_hierarchy[wrong_name]["scientific name"]["synonymous"] = gbif_suggest[index]["synonym"]
                        if gbif_suggest[index]["synonym"] == "true":
                            self.verified_hierarchy[wrong_name]["scientific name"]["synonym"] = gbif_suggest[index]["usageKey"]
                        
                        self.verified_hierarchy[wrong_name]["scientific name"]["accept"] = gbif_suggest[index]["speciesKey"]
                        self.verified_hierarchy[wrong_name]["scientific name"]["canonicalname"] = gbif_suggest[index]["canonicalName"]
                        self.verified_hierarchy[wrong_name]["scientific name"]["speciesname"] = gbif_suggest[index]["species"]

    def set_Verified_Hierarchy(self, hierarchy):
        self.verified_hierarchy = hierarchy

    def get_Verified_Hierarchy (self):
        return self.verified_hierarchy

    def String_Occurrence_Column (self, column):
        check_column = self.sheet.col_values(column, 1)
        checked_column = {}
        for name in check_column:
            if name in checked_column:
                continue
            else:
                checked_column[name] = {"amount": check_column.count(name)}
        return checked_column

    def Compare_String (self, String1, String2):

        Ratio_value = fuzz.ratio(String1.lower(), String2.lower())
        Partial_Ratio_value = fuzz.partial_ratio(String1.lower(), String2.lower())
        Token_Sort_Ratio_value = fuzz.token_sort_ratio(String1, String2)
        Token_Set_Ratio_value = fuzz.token_set_ratio(String1, String2)
        Mean = (Ratio_value + Partial_Ratio_value + Token_Sort_Ratio_value + Token_Set_Ratio_value) / 4

        return Mean

    def String_Similarity(self, column):

        if type(column) == int:

            check_column = self.String_Occurrence_Column(column)

        elif type(column) == str:
            index_column = self.sheet.row_values(0).index(column)
            check_column = self.String_Occurrence_Column(index_column)
        for string1 in check_column:
            suggest = []
            for string2 in check_column:
                if self.Compare_String (string1, string2) > 60 and string1 != string2:
                    suggest.append({"Similarity": self.Compare_String (string1, string2), "Suggestion": string2})
            check_column[string1]["Suggestion"] = suggest
        return check_column

    def String_Similarity_2(self, string, column):
        result = process.extract(string, column, scorer=fuzz.partial_token_set_ratio, limit=10)
        return result
