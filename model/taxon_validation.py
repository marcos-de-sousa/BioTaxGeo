from model.hierarchy_taxon import Hierarchy_Taxon
class Taxon_Validation(Hierarchy_Taxon):

    def __init__(self, k=None, p=None, c=None, o=None, f=None, sf=None, g=None, sg=None, e=None, se=None, sn=None):
        super().__init__(k, p, c, o, f, sf, g, sg, e, se, sn)
        self.kingdom_correctness = "NONE"
        self.phylum_correctness = "NONE"
        self.class_correctness = "NONE"
        self.order_correctness = "NONE"
        self.family_correctness = "NONE"
        self.genus_correctness = "NONE"
        self.specie_correctness = "NONE"
        self.scientific_name_correctness = "NONE"
        self.kingdom_suggestion = []
        self.phylum_suggestion = []
        self.classs_suggestion = []
        self.order_suggestion = []
        self.family_suggestion = []
        self.genus_suggestion = []
        self.specie_suggestion = []
        self.scientific_name_suggestion = []

    def set_Hierarchy (self, k, p, c, o, f, g, e, SN):
        self.Scientific_Name = SN
        self.kingdom = k
        self.phylum = p
        self.classs = c
        self.order = o
        self.family = f
        self.genus = g
        self.specie = e

    def get_Hierarchy (self):
        return self.kingdom, self.phylum, self.order, self.family, self.genus, self.specie, self.Scientific_Name

    def set_Hierarchy_Correctness (self, kingdom, phylum, classs, order, family, genus, specie, Scientific_Name):
        self.kingdom_correctness = "EXACT" if (self.kingdom == kingdom) else "FUZZY"
        self.phylum_correctness = "EXACT" if self.phylum == phylum else "FUZZY"
        self.class_correctness = "EXACT" if self.classs == classs else "FUZZY"
        self.order_correctness = "EXACT" if self.order == order else "FUZZY"
        self.family_correctness = "EXACT" if self.family == family else "FUZZY"
        self.genus_correctness = "EXACT" if self.genus == genus else "FUZZY"
        if (self.specie == specie.replace(genus + " ", "")) or (self.specie == specie.replace(self.genus + " ", "")):
            self.specie_correctness = "EXACT"
        else:
            self.specie_correctness = "FUZZY"
        self.scientific_name_correctness = "EXACT" if self.Scientific_Name == Scientific_Name else "FUZZY"

    def set_Hierarchy_Suggestion (self, kingdom, phylum, classs, order, family, genus, specie, Scientific_Name):
        self.kingdom_suggestion = None if self.kingdom_correctness == "EXACT" else kingdom
        self.phylum_suggestion = None if self.phylum_correctness == "EXACT" else phylum
        self.classs_suggestion = None if self.class_correctness == "EXACT" else classs
        self.order_suggestion = None if self.order_correctness == "EXACT" else order
        self.family_suggestion = None if self.family_correctness == "EXACT" else family
        self.genus_suggestion = None if self.genus_correctness == "EXACT" else genus
        if self.specie_correctness == "EXACT":
            self.specie_suggestion = None
        else:
            self.specie_suggestion = specie.replace(genus + " ", "") if genus in specie else specie.replace(self.genus + " ", "")
        self.scientific_name_suggestion = None if self.scientific_name_correctness == "EXACT" else Scientific_Name


    def get_Scientific_Name(self):
        return self.Scientific_Name

    def get_Kingdom_Correctness(self):
        return self.kingdom_correctness

    def get_Phylum_Correctness(self):
        return self.phylum_correctness

    def get_Classs_Correctness(self):
        return self.class_correctness

    def get_Order_Correctness(self):
        return self.order_correctness

    def get_Family_Correctness(self):
        return self.family_correctness

    def get_Genus_Correctness(self):
        return self.genus_correctness

    def get_Specie_Correctness(self):
        return self.specie_correctness

    def get_Scientific_Name_Correctness(self):
        return self.scientific_name_correctness

    def get_Kingdom_Suggestion(self):
        return self.kingdom_suggestion

    def get_Phylum_Suggestion(self):
        return self.phylum_suggestion

    def get_Classs_Suggestion(self):
        return self.classs_suggestion

    def get_Order_Suggestion(self):
        return self.order_suggestion

    def get_Family_Suggestion(self):
        return self.family_suggestion

    def get_Genus_Suggestion(self):
        return self.genus_suggestion

    def get_Specie_Suggestion(self):
        return self.specie_suggestion

    def get_Scientific_Name_Suggestion(self):
        return self.scientific_name_suggestion