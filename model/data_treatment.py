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
                                                         p=check_hrch['phylum'][index],
                                                         c=check_hrch['class'][index],
                                                         o=check_hrch['order'][index],
                                                         f=check_hrch['family'][index],
                                                         g=check_hrch['genus'][index],
                                                         e=check_hrch['specie'][index],
                                                         sn=Scientific_Name
                                                        )

                if Scientific_Name in self.get_Verified_Hierarchy():
                    continue
                else:

                    globalnames = self.get_GlobalNames(Scientific_Name)
                    if Scientific_Name == "Nessaea obrina":
                        print(globalnames)
                    if (globalnames):
                        self.verified_hierarchy[Scientific_Name] = {
                            "kingdom": {
                                "type": self.taxon_validation.get_Kingdom(),
                                "correctness": None,
                                "amount": check_hrch['kingdom'].count(self.taxon_validation.get_Kingdom()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[0],
                                "sources": {},
                                "score": []

                            },
                            "phylum": {
                                "type": self.taxon_validation.get_Phylum(),
                                "correctness": None,
                                "amount": check_hrch['phylum'].count(self.taxon_validation.get_Phylum()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[1],
                                "sources": {},
                                "score": []
                            },
                            "class": {
                                "type": self.taxon_validation.get_Classs(),
                                "correctness": None,
                                "amount": check_hrch['class'].count(self.taxon_validation.get_Classs()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[2],
                                "sources": {},
                                "score": []
                            },
                            "order": {
                                "type": self.taxon_validation.get_Order(),
                                "correctness": None,
                                "amount": check_hrch['order'].count(self.taxon_validation.get_Order()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[3],
                                "sources": {},
                                "score": []
                            },
                            "family": {
                                "type": self.taxon_validation.get_Family(),
                                "correctness": None,
                                "amount": check_hrch['family'].count(self.taxon_validation.get_Family()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[4],
                                "sources": {},
                                "score": []
                            },
                            "genus": {
                                "type": self.taxon_validation.get_Genus(),
                                "correctness": None,
                                "amount": check_hrch['genus'].count(self.taxon_validation.get_Genus()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[5],
                                "sources": {},
                                "score": []
                            },
                            "specie": {
                                "type": self.taxon_validation.get_Specie(),
                                "correctness": None,
                                "amount": check_hrch['specie'].count(self.taxon_validation.get_Specie()),
                                "suggestion": [],
                                "title": self.get_Original_Titles()[6],
                                "sources": {},
                                "score": []
                            },
                            "scientific name": {
                                "type": self.taxon_validation.get_Scientific_Name(),
                                "correctness": self.taxon_validation.get_Scientific_Name_Correctness(),
                                "suggestion": [],
                                "synonymous": False,
                                "font": "",
                                "synonym": False,
                                "accept": "",
                                "canonicalname": [],
                                "speciesname": [],
                                "list_fonts": None,
                                "sources": {},
                                "score": []
                            }
                        }

                        for key in globalnames:

                            self.taxon_validation.set_Hierarchy_Correctness(
                                                                            globalnames[key]["Rank"]["kingdom"],
                                                                            globalnames[key]["Rank"]["phylum"],
                                                                            globalnames[key]["Rank"]["class"],
                                                                            globalnames[key]["Rank"]["order"],
                                                                            globalnames[key]["Rank"]["family"],
                                                                            globalnames[key]["Rank"]["genus"],
                                                                            globalnames[key]["Rank"]["species"],
                                                                            globalnames[key]["Canonical_form"]
                                                                           )

                            self.taxon_validation.set_Hierarchy_Suggestion(
                                                                            globalnames[key]["Rank"]["kingdom"],
                                                                            globalnames[key]["Rank"]["phylum"],
                                                                            globalnames[key]["Rank"]["class"],
                                                                            globalnames[key]["Rank"]["order"],
                                                                            globalnames[key]["Rank"]["family"],
                                                                            globalnames[key]["Rank"]["genus"],
                                                                            globalnames[key]["Rank"]["species"],
                                                                            globalnames[key]["Canonical_form"]
                                                                          )
                            hierarchy_suggestion = self.taxon_validation.get_Suggestion_Hierarchy()
                            hierarchy_correctness = self.taxon_validation.get_Correctness_Hierarchy()
                            hierarchy_keys = list(self.verified_hierarchy[Scientific_Name].keys())

                            for i in range(len(hierarchy_suggestion)):
                                k = hierarchy_keys[i]
                                if hierarchy_suggestion[i] != None and hierarchy_suggestion[i] not in self.verified_hierarchy[Scientific_Name][k]["suggestion"]:
                                    self.verified_hierarchy[Scientific_Name][k]["suggestion"].append(hierarchy_suggestion[i])
                                    self.verified_hierarchy[Scientific_Name][k]["sources"][hierarchy_suggestion[i]] = {"source": [key], "score":[globalnames[key]["score"]]}

                                elif hierarchy_suggestion[i] in self.verified_hierarchy[Scientific_Name][k]["suggestion"]:
                                    self.verified_hierarchy[Scientific_Name][k]["sources"][hierarchy_suggestion[i]]["source"].append(key)
                                    self.verified_hierarchy[Scientific_Name][k]["sources"][hierarchy_suggestion[i]]["score"].append(globalnames[key]["score"])
                                self.verified_hierarchy[Scientific_Name][k]["correctness"] = hierarchy_correctness[i]
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
                                "correctness": "None",
                                "suggestion": self.taxon_validation.get_Scientific_Name_Suggestion(),
                                "synonymous": "",
                                "font": "Planilha",
                                "synonym": "",
                                "accept": "",
                                "canonicalname": "",
                                "speciesname": "",
                                "list_fonts": []
                            }
                        }
        for wrong_name in self.verified_hierarchy:
            if self.verified_hierarchy[wrong_name]["scientific name"]["correctness"] == "None":
                if globalnames == False:
                    average_hierarchy_values = {}
                    for correct_name in self.verified_hierarchy:
                        average_hierarchy_values[correct_name] = {}
                        for key in self.verified_hierarchy[correct_name]:
                            average_hierarchy_values[correct_name][key] = {}
                            if self.verified_hierarchy[correct_name][key]["correctness"] == "EXACT" and key != "scientific name":
                                correct = self.verified_hierarchy[correct_name][key]["type"]
                                wrong = self.verified_hierarchy[wrong_name][key]["type"]
                                average_hierarchy_values[correct_name][key][correct] = None
                                if (self.Compare_String (wrong, correct) > 40 and wrong != correct):
                                    if correct not in self.verified_hierarchy[wrong_name][key]["suggestion"]:
                                        self.verified_hierarchy[wrong_name][key]["suggestion"].append(correct)
                                    self.verified_hierarchy[wrong_name]["scientific name"]["font"] = "Planilha"
                                if (correct == wrong):
                                    self.verified_hierarchy[wrong_name][key]["correctness"] = self.verified_hierarchy[correct_name][key]["correctness"]



    def set_Verified_Hierarchy(self, hierarchy):
        self.verified_hierarchy = hierarchy

    def get_GlobalNames(self, name):
        import requests
        result = requests.get('http://resolver.globalnames.org/name_resolvers.json?names={}'.format(name)).json()
        if "results" in result["data"][0]:
            is_known_name = result["data"][0]["is_known_name"]
            result = result["data"][0]["results"]

        else:
            return False
        Bases = {}
        lvl_rank = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
        for y in result:
            if (y['classification_path'] != "") and (y['data_source_title'] not in Bases) and (y['classification_path'] != None):
                rank_list = y['classification_path_ranks'].split("|")
                classification_list = y['classification_path'].split("|")
                Bases[y['data_source_title']] = {"Canonical_form": y['canonical_form'], "Rank": {}, "score": y['score'], "is_known_name": is_known_name}
                for r in range(len(rank_list)):
                    Bases[y['data_source_title']]["Rank"].update({rank_list[r]: classification_list[r]})
                lvls = Bases[y['data_source_title']]["Rank"].keys()
                for r in lvl_rank:
                    if r not in lvls:
                        Bases.pop(y['data_source_title'], 10)
        return Bases

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
