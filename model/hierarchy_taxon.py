class Hierarchy_Taxon:
       def __init__(self, k=None, p=None, c=None, o=None, f=None, sf=None, g=None, sg=None, e=None, se=None, sn=None):
              self.Scientific_Name = sn
              self.kingdom = k
              self.phylum = p
              self.classs = c
              self.order = o
              self.family = f
              self.subfamily = sf
              self.genus = g
              self.subgenus = sg
              self.specie = e
              self.subspecie =se

       def get_Kingdom(self):
              return self.kingdom

       def get_Phylum(self):
              return self.phylum

       def get_Classs(self):
              return self.classs

       def get_Order(self):
              return self.order

       def get_Family(self):
              return self.family

       def get_SubFamily(self):
              return self.subfamily

       def get_Genus(self):
              return self.genus

       def get_SubGenus(self):
              return self.subgenus

       def get_Specie(self):
              return self.specie

       def get_SubSpecie(self):
              return self.subspecie

       def get_ScientificName(self):
              return self.Scientific_Name

       def set_Kingdom(self, k):
              self.kingdom = k

       def set_Phylum(self, p):
              self.phylum = p

       def set_Classs(self, c):
              self.classs = c

       def set_Order(self, o):
              self.order = o

       def set_Family(self, f):
              self.family = f

       def set_SubFamily(self, sf):
              self.subfamily = sf

       def set_Genus(self, g):
              self.genus = g

       def set_SubGenus(self, sg):
              self.subgenus = sg

       def set_Specie(self, s):
              self.specie = s

       def set_SubSpecie(self, ss):
              self.subspecie = ss

       def set_ScientificName(self, sn):
              self.Scientific_Name = sn